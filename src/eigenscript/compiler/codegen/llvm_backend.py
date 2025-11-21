"""
LLVM Backend for EigenScript Compiler
Generates LLVM IR from EigenScript AST nodes.
"""

from llvmlite import ir
from llvmlite import binding as llvm
from typing import Dict, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass

from eigenscript.parser.ast_builder import (
    ASTNode,
    Literal,
    Identifier,
    BinaryOp,
    UnaryOp,
    Assignment,
    FunctionDef,
    Return,
    Break,
    Conditional,
    Loop,
    Relation,
    Interrogative,
    ListLiteral,
    Index,
    Slice,
    Program,
)


class ValueKind(Enum):
    """Tracks the kind of value generated during compilation."""

    SCALAR = "scalar"  # Raw double value
    EIGEN_PTR = "eigen_ptr"  # EigenValue* pointer
    LIST_PTR = "list_ptr"  # EigenList* pointer


@dataclass
class GeneratedValue:
    """Wrapper for values generated during compilation.

    This enables Option 2 (interrogative aliasing) by tracking whether
    a value is a raw scalar or an EigenValue pointer, preserving the
    is/of duality where 'of' is observational (stable) and 'is' is computational.
    """

    value: ir.Value
    kind: ValueKind


class LLVMCodeGenerator:
    """Generates LLVM IR from EigenScript AST."""

    def __init__(self):
        # Initialize LLVM targets (initialization is now automatic in llvmlite)
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create module and builder
        self.module = ir.Module(name="eigenscript_module")
        self.module.triple = llvm.get_default_triple()

        # Type definitions
        self.double_type = ir.DoubleType()
        self.int64_type = ir.IntType(64)
        self.int32_type = ir.IntType(32)
        self.int8_type = ir.IntType(8)
        self.void_type = ir.VoidType()
        self.bool_type = ir.IntType(1)

        # EigenValue structure: {double value, double gradient, double stability, i64 iteration}
        self.eigen_value_type = ir.LiteralStructType(
            [
                self.double_type,  # value
                self.double_type,  # gradient (why)
                self.double_type,  # stability (how)
                self.int64_type,  # iteration (when)
            ]
        )

        # EigenList structure: {double* data, i64 length, i64 capacity}
        self.eigen_list_type = ir.LiteralStructType(
            [
                self.double_type.as_pointer(),  # data
                self.int64_type,  # length
                self.int64_type,  # capacity
            ]
        )

        # Pointer types
        self.eigen_value_ptr = self.eigen_value_type.as_pointer()
        self.eigen_list_ptr = self.eigen_list_type.as_pointer()
        self.string_type = self.int8_type.as_pointer()

        # Symbol tables
        self.global_vars: Dict[str, ir.AllocaInstr] = {}
        self.local_vars: Dict[str, ir.AllocaInstr] = {}
        self.functions: Dict[str, ir.Function] = {}

        # Current function and builder
        self.current_function: Optional[ir.Function] = None
        self.builder: Optional[ir.IRBuilder] = None

        # Initialize runtime functions
        self._declare_runtime_functions()

    def _declare_runtime_functions(self):
        """Declare external runtime functions for geometric state tracking."""

        # printf for debugging
        printf_type = ir.FunctionType(self.int32_type, [self.string_type], var_arg=True)
        self.printf = ir.Function(self.module, printf_type, name="printf")

        # malloc for dynamic allocation
        malloc_type = ir.FunctionType(self.string_type, [self.int64_type])
        self.malloc = ir.Function(self.module, malloc_type, name="malloc")

        # Runtime functions for geometric tracking
        # eigen_create(value) -> EigenValue*
        eigen_create_type = ir.FunctionType(self.eigen_value_ptr, [self.double_type])
        self.eigen_create = ir.Function(
            self.module, eigen_create_type, name="eigen_create"
        )

        # eigen_update(eigen*, new_value) -> void
        eigen_update_type = ir.FunctionType(
            self.void_type, [self.eigen_value_ptr, self.double_type]
        )
        self.eigen_update = ir.Function(
            self.module, eigen_update_type, name="eigen_update"
        )

        # eigen_get_value(eigen*) -> double
        eigen_get_value_type = ir.FunctionType(self.double_type, [self.eigen_value_ptr])
        self.eigen_get_value = ir.Function(
            self.module, eigen_get_value_type, name="eigen_get_value"
        )

        # eigen_get_gradient(eigen*) -> double (for 'why')
        eigen_get_gradient_type = ir.FunctionType(
            self.double_type, [self.eigen_value_ptr]
        )
        self.eigen_get_gradient = ir.Function(
            self.module, eigen_get_gradient_type, name="eigen_get_gradient"
        )

        # eigen_get_stability(eigen*) -> double (for 'how')
        eigen_get_stability_type = ir.FunctionType(
            self.double_type, [self.eigen_value_ptr]
        )
        self.eigen_get_stability = ir.Function(
            self.module, eigen_get_stability_type, name="eigen_get_stability"
        )

        # eigen_get_iteration(eigen*) -> i64 (for 'when')
        eigen_get_iteration_type = ir.FunctionType(
            self.int64_type, [self.eigen_value_ptr]
        )
        self.eigen_get_iteration = ir.Function(
            self.module, eigen_get_iteration_type, name="eigen_get_iteration"
        )

        # eigen_check_converged(eigen*) -> bool
        eigen_check_converged_type = ir.FunctionType(
            self.bool_type, [self.eigen_value_ptr]
        )
        self.eigen_check_converged = ir.Function(
            self.module, eigen_check_converged_type, name="eigen_check_converged"
        )

        # eigen_check_diverging(eigen*) -> bool
        eigen_check_diverging_type = ir.FunctionType(
            self.bool_type, [self.eigen_value_ptr]
        )
        self.eigen_check_diverging = ir.Function(
            self.module, eigen_check_diverging_type, name="eigen_check_diverging"
        )

        # eigen_check_oscillating(eigen*) -> bool
        eigen_check_oscillating_type = ir.FunctionType(
            self.bool_type, [self.eigen_value_ptr]
        )
        self.eigen_check_oscillating = ir.Function(
            self.module, eigen_check_oscillating_type, name="eigen_check_oscillating"
        )

        # eigen_check_stable(eigen*) -> bool
        eigen_check_stable_type = ir.FunctionType(
            self.bool_type, [self.eigen_value_ptr]
        )
        self.eigen_check_stable = ir.Function(
            self.module, eigen_check_stable_type, name="eigen_check_stable"
        )

        # eigen_check_improving(eigen*) -> bool
        eigen_check_improving_type = ir.FunctionType(
            self.bool_type, [self.eigen_value_ptr]
        )
        self.eigen_check_improving = ir.Function(
            self.module, eigen_check_improving_type, name="eigen_check_improving"
        )

        # List runtime functions
        # eigen_list_create(length) -> EigenList*
        eigen_list_create_type = ir.FunctionType(self.eigen_list_ptr, [self.int64_type])
        self.eigen_list_create = ir.Function(
            self.module, eigen_list_create_type, name="eigen_list_create"
        )

        # eigen_list_get(list*, index) -> double
        eigen_list_get_type = ir.FunctionType(
            self.double_type, [self.eigen_list_ptr, self.int64_type]
        )
        self.eigen_list_get = ir.Function(
            self.module, eigen_list_get_type, name="eigen_list_get"
        )

        # eigen_list_set(list*, index, value) -> void
        eigen_list_set_type = ir.FunctionType(
            self.void_type, [self.eigen_list_ptr, self.int64_type, self.double_type]
        )
        self.eigen_list_set = ir.Function(
            self.module, eigen_list_set_type, name="eigen_list_set"
        )

        # eigen_list_length(list*) -> i64
        eigen_list_length_type = ir.FunctionType(self.int64_type, [self.eigen_list_ptr])
        self.eigen_list_length = ir.Function(
            self.module, eigen_list_length_type, name="eigen_list_length"
        )

    def ensure_scalar(self, gen_val: Union[GeneratedValue, ir.Value]) -> ir.Value:
        """Convert a GeneratedValue to a scalar double.

        This is used when arithmetic, comparisons, or printing need raw values.
        If given an EigenValue* pointer, extracts the value field.
        If given a raw ir.Value, assumes it's already a scalar and returns it.
        """
        # Backward compatibility: if passed raw ir.Value, assume it's a scalar
        if isinstance(gen_val, ir.Value):
            return gen_val

        if gen_val.kind == ValueKind.SCALAR:
            return gen_val.value
        elif gen_val.kind == ValueKind.EIGEN_PTR:
            # Dereference the EigenValue* to get the value
            return self.builder.call(self.eigen_get_value, [gen_val.value])
        elif gen_val.kind == ValueKind.LIST_PTR:
            raise TypeError("Cannot convert list to scalar")
        else:
            raise ValueError(f"Unknown ValueKind: {gen_val.kind}")

    def ensure_eigen_ptr(self, gen_val: Union[GeneratedValue, ir.Value]) -> ir.Value:
        """Convert a GeneratedValue to an EigenValue* pointer.

        This is used when we need to store or pass geometric state.
        If given a scalar, wraps it in a new EigenValue.
        If given an EigenValue*, returns it directly (enabling aliasing).
        """
        # Backward compatibility: if passed raw ir.Value, assume it's a scalar
        if isinstance(gen_val, ir.Value):
            return self.builder.call(self.eigen_create, [gen_val])

        if gen_val.kind == ValueKind.SCALAR:
            # Wrap scalar in new EigenValue
            return self.builder.call(self.eigen_create, [gen_val.value])
        elif gen_val.kind == ValueKind.EIGEN_PTR:
            # Already a pointer, return directly (this enables aliasing!)
            return gen_val.value
        elif gen_val.kind == ValueKind.LIST_PTR:
            raise TypeError("Cannot convert list to EigenValue")
        else:
            raise ValueError(f"Unknown ValueKind: {gen_val.kind}")

    def compile(self, ast_nodes: list[ASTNode]) -> str:
        """Compile a list of AST nodes to LLVM IR."""

        # Create main function
        main_type = ir.FunctionType(self.int32_type, [])
        main_func = ir.Function(self.module, main_type, name="main")
        block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.current_function = main_func

        # Generate code for each statement
        for node in ast_nodes:
            self._generate(node)

        # Return 0 from main
        self.builder.ret(ir.Constant(self.int32_type, 0))

        return str(self.module)

    def _generate(self, node: ASTNode) -> ir.Value:
        """Generate LLVM IR for an AST node."""

        if isinstance(node, Literal):
            return self._generate_literal(node)
        elif isinstance(node, Identifier):
            return self._generate_identifier(node)
        elif isinstance(node, BinaryOp):
            return self._generate_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self._generate_unary_op(node)
        elif isinstance(node, Assignment):
            return self._generate_assignment(node)
        elif isinstance(node, Relation):
            return self._generate_relation(node)
        elif isinstance(node, Conditional):
            return self._generate_conditional(node)
        elif isinstance(node, Loop):
            return self._generate_loop(node)
        elif isinstance(node, Interrogative):
            return self._generate_interrogative(node)
        elif isinstance(node, FunctionDef):
            return self._generate_function_def(node)
        elif isinstance(node, Return):
            return self._generate_return(node)
        elif isinstance(node, ListLiteral):
            return self._generate_list_literal(node)
        elif isinstance(node, Index):
            return self._generate_index(node)
        else:
            raise NotImplementedError(
                f"Code generation for {type(node).__name__} not implemented"
            )

    def _generate_literal(self, node: Literal) -> ir.Value:
        """Generate code for a literal value."""
        if node.literal_type == "number":
            return ir.Constant(self.double_type, float(node.value))
        elif node.literal_type == "string":
            # String literals - create global constant
            string_val = node.value + "\0"
            string_const = ir.Constant(
                ir.ArrayType(self.int8_type, len(string_val)),
                bytearray(string_val.encode("utf-8")),
            )
            global_str = ir.GlobalVariable(
                self.module, string_const.type, name=f"str_{id(node)}"
            )
            global_str.global_constant = True
            global_str.initializer = string_const
            return self.builder.bitcast(global_str, self.string_type)
        else:
            raise NotImplementedError(
                f"Literal type {node.literal_type} not implemented"
            )

    def _generate_identifier(self, node: Identifier) -> ir.Value:
        """Generate code for variable access."""
        # Check if this is a predicate
        if node.name in [
            "converged",
            "diverging",
            "oscillating",
            "stable",
            "improving",
        ]:
            # Get the last assigned variable (simplified - should be explicit in real code)
            if self.local_vars:
                last_var_name = list(self.local_vars.keys())[-1]
                var_ptr = self.local_vars[last_var_name]
                eigen_ptr = self.builder.load(var_ptr)

                # Call the appropriate predicate function
                if node.name == "converged":
                    return self.builder.call(self.eigen_check_converged, [eigen_ptr])
                elif node.name == "diverging":
                    return self.builder.call(self.eigen_check_diverging, [eigen_ptr])
                elif node.name == "oscillating":
                    return self.builder.call(self.eigen_check_oscillating, [eigen_ptr])
                elif node.name == "stable":
                    return self.builder.call(self.eigen_check_stable, [eigen_ptr])
                elif node.name == "improving":
                    return self.builder.call(self.eigen_check_improving, [eigen_ptr])

        if node.name in self.local_vars:
            var_ptr = self.local_vars[node.name]
        elif node.name in self.global_vars:
            var_ptr = self.global_vars[node.name]
        else:
            raise NameError(f"Undefined variable: {node.name}")

        # Load the pointer
        loaded_ptr = self.builder.load(var_ptr)

        # Check if it's a list
        if isinstance(loaded_ptr.type, ir.PointerType):
            pointed_type = loaded_ptr.type.pointee
            if (
                isinstance(pointed_type, ir.LiteralStructType)
                and len(pointed_type.elements) == 3
                and isinstance(pointed_type.elements[0], ir.PointerType)
            ):
                # It's a list - return the pointer directly
                return loaded_ptr

        # It's an EigenValue - get the actual value
        return self.builder.call(self.eigen_get_value, [loaded_ptr])

    def _generate_binary_op(self, node: BinaryOp) -> ir.Value:
        """Generate code for binary operations.

        Binary ops need scalar values, so we convert both operands using ensure_scalar().
        This allows mixing literals, variables, and interrogative results seamlessly.
        """
        left_gen = self._generate(node.left)
        right_gen = self._generate(node.right)

        # Convert to scalars (handles aliases from interrogatives)
        left = self.ensure_scalar(left_gen)
        right = self.ensure_scalar(right_gen)

        if node.operator == "+":
            return self.builder.fadd(left, right)
        elif node.operator == "-":
            return self.builder.fsub(left, right)
        elif node.operator == "*":
            return self.builder.fmul(left, right)
        elif node.operator == "/":
            return self.builder.fdiv(left, right)
        elif node.operator == ">":
            return self.builder.fcmp_ordered(">", left, right)
        elif node.operator == "<":
            return self.builder.fcmp_ordered("<", left, right)
        elif node.operator == "==":
            return self.builder.fcmp_ordered("==", left, right)
        elif node.operator == "!=":
            return self.builder.fcmp_ordered("!=", left, right)
        else:
            raise NotImplementedError(
                f"Binary operator {node.operator} not implemented"
            )

    def _generate_unary_op(self, node: UnaryOp) -> ir.Value:
        """Generate code for unary operations."""
        # Check if operand is a predicate (converged, diverging, etc.)
        if isinstance(node.operand, Identifier):
            predicate_name = node.operand.name

            # Special handling for predicates - they implicitly refer to a variable
            # For now, we'll check all variables for the predicate
            # In a full implementation, predicates would be bound to specific variables

            if predicate_name in [
                "converged",
                "diverging",
                "oscillating",
                "stable",
                "improving",
            ]:
                # Get the last assigned variable (simplified - should be explicit in real code)
                if self.local_vars:
                    # Get the most recently created variable
                    last_var_name = list(self.local_vars.keys())[-1]
                    var_ptr = self.local_vars[last_var_name]
                    eigen_ptr = self.builder.load(var_ptr)

                    # Call the appropriate predicate function
                    if predicate_name == "converged":
                        result = self.builder.call(
                            self.eigen_check_converged, [eigen_ptr]
                        )
                    elif predicate_name == "diverging":
                        result = self.builder.call(
                            self.eigen_check_diverging, [eigen_ptr]
                        )
                    elif predicate_name == "oscillating":
                        result = self.builder.call(
                            self.eigen_check_oscillating, [eigen_ptr]
                        )
                    elif predicate_name == "stable":
                        result = self.builder.call(self.eigen_check_stable, [eigen_ptr])
                    elif predicate_name == "improving":
                        result = self.builder.call(
                            self.eigen_check_improving, [eigen_ptr]
                        )
                    else:
                        raise NotImplementedError(
                            f"Predicate {predicate_name} not implemented"
                        )

                    # Apply NOT operator if present
                    if node.operator == "not":
                        result = self.builder.not_(result)

                    return result

        # General unary operation
        operand = self._generate(node.operand)

        if node.operator == "not":
            # Logical NOT
            return self.builder.not_(operand)
        elif node.operator == "-":
            # Numeric negation
            return self.builder.fneg(operand)
        else:
            raise NotImplementedError(f"Unary operator {node.operator} not implemented")

    def _generate_assignment(self, node: Assignment) -> None:
        """Generate code for variable assignment.

        Handles both scalar updates and pointer aliasing (Option 2).
        If RHS is an EigenValue* (from interrogative), creates an alias.
        If RHS is a scalar, updates or creates a new EigenValue.
        """
        gen_value = self._generate(node.expression)

        # Handle backward compatibility: convert raw ir.Value to GeneratedValue
        if isinstance(gen_value, ir.Value):
            # Detect if it's a list
            is_list = False
            if isinstance(gen_value.type, ir.PointerType):
                pointed_type = gen_value.type.pointee
                if (
                    isinstance(pointed_type, ir.LiteralStructType)
                    and len(pointed_type.elements) == 3
                    and isinstance(pointed_type.elements[0], ir.PointerType)
                ):
                    is_list = True

            if is_list:
                gen_value = GeneratedValue(value=gen_value, kind=ValueKind.LIST_PTR)
            else:
                # Assume it's a scalar
                gen_value = GeneratedValue(value=gen_value, kind=ValueKind.SCALAR)

        # Handle list assignment
        if gen_value.kind == ValueKind.LIST_PTR:
            var_ptr = self.builder.alloca(self.eigen_list_ptr, name=node.identifier)
            self.builder.store(gen_value.value, var_ptr)
            self.local_vars[node.identifier] = var_ptr
            return

        # Handle EigenValue assignment (scalar or pointer)
        if node.identifier in self.local_vars:
            # Variable exists - update or rebind
            if gen_value.kind == ValueKind.EIGEN_PTR:
                # Aliasing: rebind to point to the same EigenValue*
                # This is the key to Option 2: "value is what is x" makes value an alias
                self.builder.store(gen_value.value, self.local_vars[node.identifier])
            else:
                # Scalar update: update existing variable's value
                eigen_ptr = self.builder.load(self.local_vars[node.identifier])
                scalar_val = self.ensure_scalar(gen_value)
                self.builder.call(self.eigen_update, [eigen_ptr, scalar_val])
        else:
            # Create new variable
            eigen_ptr = self.ensure_eigen_ptr(gen_value)
            var_ptr = self.builder.alloca(self.eigen_value_ptr, name=node.identifier)
            self.builder.store(eigen_ptr, var_ptr)
            self.local_vars[node.identifier] = var_ptr

    def _generate_relation(self, node: Relation) -> ir.Value:
        """Generate code for relations (function calls via 'of' operator)."""
        # Check if left side is a function name
        if isinstance(node.left, Identifier):
            func_name = node.left.name

            # Handle built-in functions
            if func_name == "print":
                arg_gen_val = self._generate(node.right)
                # Convert to scalar for printing (handles both raw values and aliases)
                arg_val = self.ensure_scalar(arg_gen_val)
                # Print format string
                fmt_str = "%f\n\0"
                fmt_const = ir.Constant(
                    ir.ArrayType(self.int8_type, len(fmt_str)),
                    bytearray(fmt_str.encode("utf-8")),
                )
                global_fmt = ir.GlobalVariable(
                    self.module, fmt_const.type, name=f"fmt_{id(node)}"
                )
                global_fmt.global_constant = True
                global_fmt.initializer = fmt_const
                fmt_ptr = self.builder.bitcast(global_fmt, self.string_type)
                return self.builder.call(self.printf, [fmt_ptr, arg_val])

            # Handle user-defined functions
            if func_name in self.functions:
                # Get the argument and convert to EigenValue*
                arg = node.right

                # If argument is an identifier, get its EigenValue pointer directly
                if isinstance(arg, Identifier):
                    if arg.name in self.local_vars or arg.name in self.global_vars:
                        var_ptr = self.local_vars.get(arg.name) or self.global_vars.get(
                            arg.name
                        )
                        eigen_ptr = self.builder.load(var_ptr)
                    else:
                        raise NameError(f"Undefined variable: {arg.name}")
                else:
                    # For other expressions (including interrogatives), generate and convert
                    arg_gen_val = self._generate(arg)
                    # Use helper to convert to EigenValue* (handles both scalars and pointers)
                    eigen_ptr = self.ensure_eigen_ptr(arg_gen_val)

                # Call the function
                func = self.functions[func_name]
                result = self.builder.call(func, [eigen_ptr])
                return result

        raise NotImplementedError(
            f"Relation {node.left} of {node.right} not implemented"
        )

    def _generate_conditional(self, node: Conditional) -> None:
        """Generate code for if-else statements."""
        cond = self._generate(node.condition)

        # Create basic blocks
        then_block = self.current_function.append_basic_block(name="if.then")
        else_block = (
            self.current_function.append_basic_block(name="if.else")
            if node.else_block
            else None
        )
        merge_block = self.current_function.append_basic_block(name="if.end")

        # Branch based on condition
        if else_block:
            self.builder.cbranch(cond, then_block, else_block)
        else:
            self.builder.cbranch(cond, then_block, merge_block)

        # Generate then block
        self.builder.position_at_end(then_block)
        then_terminated = False
        for stmt in node.if_block:
            self._generate(stmt)
            if isinstance(stmt, Return):
                then_terminated = True
                break
        if not then_terminated:
            self.builder.branch(merge_block)

        # Generate else block if present
        else_terminated = False
        if else_block:
            self.builder.position_at_end(else_block)
            for stmt in node.else_block:
                self._generate(stmt)
                if isinstance(stmt, Return):
                    else_terminated = True
                    break
            if not else_terminated:
                self.builder.branch(merge_block)

        # Continue at merge block
        self.builder.position_at_end(merge_block)

    def _generate_loop(self, node: Loop) -> None:
        """Generate code for loops."""
        # Create basic blocks
        loop_cond = self.current_function.append_basic_block(name="loop.cond")
        loop_body = self.current_function.append_basic_block(name="loop.body")
        loop_end = self.current_function.append_basic_block(name="loop.end")

        # Jump to condition check
        self.builder.branch(loop_cond)

        # Generate condition check
        self.builder.position_at_end(loop_cond)
        cond = self._generate(node.condition)
        self.builder.cbranch(cond, loop_body, loop_end)

        # Generate loop body
        self.builder.position_at_end(loop_body)
        body_terminated = False
        for stmt in node.body:
            self._generate(stmt)
            if isinstance(stmt, Return):
                body_terminated = True
                break
        if not body_terminated:
            self.builder.branch(loop_cond)

        # Continue after loop
        self.builder.position_at_end(loop_end)

    def _generate_interrogative(self, node: Interrogative) -> GeneratedValue:
        """Generate code for interrogatives (what, who, why, how, when, where).

        Only 'what is' returns EIGEN_PTR for aliasing (Option 2).
        Other interrogatives extract specific fields and return scalars.
        This preserves the is/of duality while maintaining correct semantics.
        """
        # Interrogative has 'interrogative' field and 'expression' field
        target_expr = node.expression

        if not isinstance(target_expr, Identifier):
            raise NotImplementedError(
                "Interrogatives only support simple identifiers for now"
            )

        target_name = target_expr.name
        if target_name not in self.local_vars and target_name not in self.global_vars:
            raise NameError(f"Undefined variable: {target_name}")

        var_ptr = self.local_vars.get(target_name) or self.global_vars.get(target_name)
        eigen_ptr = self.builder.load(var_ptr)

        # Special case: 'what is' returns the pointer for aliasing
        if node.interrogative == "what":
            # Return EigenValue* pointer - enables aliasing
            # "value is what is x" makes value an alias to x
            return GeneratedValue(value=eigen_ptr, kind=ValueKind.EIGEN_PTR)

        # Other interrogatives extract specific fields and return scalars
        elif node.interrogative == "why":
            scalar_val = self.builder.call(self.eigen_get_gradient, [eigen_ptr])
            return GeneratedValue(value=scalar_val, kind=ValueKind.SCALAR)
        elif node.interrogative == "how":
            scalar_val = self.builder.call(self.eigen_get_stability, [eigen_ptr])
            return GeneratedValue(value=scalar_val, kind=ValueKind.SCALAR)
        elif node.interrogative == "when":
            # Returns i64, convert to double for consistency
            iter_count = self.builder.call(self.eigen_get_iteration, [eigen_ptr])
            scalar_val = self.builder.sitofp(iter_count, self.double_type)
            return GeneratedValue(value=scalar_val, kind=ValueKind.SCALAR)
        else:
            raise NotImplementedError(
                f"Interrogative {node.interrogative} not implemented"
            )

    def _generate_function_def(self, node: FunctionDef) -> None:
        """Generate code for function definitions."""
        # Create function signature
        # In EigenScript, functions take one EigenValue* parameter and return double
        func_type = ir.FunctionType(
            self.double_type, [self.eigen_value_ptr]  # Single parameter passed via "of"
        )

        func = ir.Function(self.module, func_type, name=node.name)
        self.functions[node.name] = func

        # Create entry block
        block = func.append_basic_block(name="entry")

        # Save current context
        prev_function = self.current_function
        prev_builder = self.builder
        prev_local_vars = self.local_vars

        # Set up new context for function
        self.current_function = func
        self.builder = ir.IRBuilder(block)
        self.local_vars = {}

        # The parameter is implicitly named 'n' in EigenScript functions
        # (convention based on examples)
        param_ptr = self.builder.alloca(self.eigen_value_ptr, name="n")
        self.builder.store(func.args[0], param_ptr)
        self.local_vars["n"] = param_ptr

        # Generate function body
        function_terminated = False
        for stmt in node.body:
            if isinstance(stmt, Return):
                self._generate(stmt)  # This will emit the ret instruction
                function_terminated = True
                break
            else:
                self._generate(stmt)

        # If no explicit return, return 0.0
        if not function_terminated:
            self.builder.ret(ir.Constant(self.double_type, 0.0))

        # Restore previous context
        self.current_function = prev_function
        self.builder = prev_builder
        self.local_vars = prev_local_vars

    def _generate_return(self, node: Return) -> ir.Value:
        """Generate code for return statements."""
        if node.expression:
            return_val = self._generate(node.expression)
            # Emit the actual return instruction
            self.builder.ret(return_val)
            return return_val
        else:
            zero = ir.Constant(self.double_type, 0.0)
            self.builder.ret(zero)
            return zero

    def _generate_list_literal(self, node: ListLiteral) -> ir.Value:
        """Generate code for list literals."""
        # Create list with length
        length = len(node.elements)
        length_val = ir.Constant(self.int64_type, length)
        list_ptr = self.builder.call(self.eigen_list_create, [length_val])

        # Set each element
        for i, elem in enumerate(node.elements):
            elem_val = self._generate(elem)
            index_val = ir.Constant(self.int64_type, i)
            self.builder.call(self.eigen_list_set, [list_ptr, index_val, elem_val])

        return list_ptr

    def _generate_index(self, node: Index) -> ir.Value:
        """Generate code for list indexing."""
        # Get the list
        list_expr = self._generate(node.list_expr)

        # Get the index
        index_expr = self._generate(node.index_expr)

        # Convert index to i64 if it's a double
        if isinstance(index_expr.type, ir.DoubleType):
            index_val = self.builder.fptosi(index_expr, self.int64_type)
        else:
            index_val = index_expr

        # Call eigen_list_get
        result = self.builder.call(self.eigen_list_get, [list_expr, index_val])
        return result

    def get_llvm_ir(self) -> str:
        """Get the generated LLVM IR as a string."""
        return str(self.module)

    def save_ir(self, filename: str):
        """Save LLVM IR to a file."""
        with open(filename, "w") as f:
            f.write(str(self.module))

    def compile_to_object(self, output_file: str):
        """Compile LLVM IR to object file."""
        llvm_ir = str(self.module)
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()

        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()

        with open(output_file, "wb") as f:
            f.write(target_machine.emit_object(mod))
