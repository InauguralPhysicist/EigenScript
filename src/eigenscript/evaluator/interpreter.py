"""
Interpreter for EigenScript.

Executes Abstract Syntax Trees using geometric transformations
in LRVM space.
"""

import numpy as np
from typing import Dict, Optional, Any, List, Union
from dataclasses import dataclass
from eigenscript.parser.ast_builder import *
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.semantic.metric import MetricTensor
from eigenscript.runtime.framework_strength import FrameworkStrengthTracker


@dataclass
class Function:
    """
    Represents a function object in EigenScript.

    Functions are timelike transformations stored with their definition
    and lexical closure.
    """
    name: str
    parameters: List[str]
    body: List[ASTNode]
    closure: "Environment"  # Captured environment

    def __repr__(self) -> str:
        return f"Function({self.name!r}, params={self.parameters})"


class ReturnValue(Exception):
    """
    Exception used to implement return statements.

    Raised when a RETURN statement is executed, carrying the return value.
    """
    def __init__(self, value: LRVMVector):
        self.value = value
        super().__init__()


class Environment:
    """
    Manages variable bindings in LRVM space.

    Supports lexical scoping with parent environments.

    Example:
        >>> env = Environment()
        >>> v = LRVMVector([1.0, 0.0, 0.0])
        >>> env.bind("x", v)
        >>> env.lookup("x")
        LRVMVector([1.0, 0.0, 0.0])
    """

    def __init__(self, parent: Optional["Environment"] = None):
        """
        Initialize environment.

        Args:
            parent: Parent environment for nested scopes
        """
        self.bindings: Dict[str, Union[LRVMVector, Function]] = {}
        self.parent = parent

    def bind(self, name: str, value: Union[LRVMVector, Function]) -> None:
        """
        Create an immutable binding.

        In EigenScript, bindings are immutable - each IS creates
        a new point in semantic spacetime rather than mutating.

        Args:
            name: Variable name
            value: LRVM vector or Function object
        """
        self.bindings[name] = value

    def lookup(self, name: str) -> Union[LRVMVector, Function]:
        """
        Resolve a variable to its LRVM vector.

        Searches current environment, then parent environments.

        Args:
            name: Variable name

        Returns:
            LRVM vector bound to the name

        Raises:
            NameError: If variable is not defined
        """
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Undefined variable: {name!r}")

    def __repr__(self) -> str:
        """String representation."""
        return f"Environment({len(self.bindings)} bindings)"


class Interpreter:
    """
    Main interpreter for EigenScript.

    Evaluates AST nodes using geometric transformations in LRVM space.

    Example:
        >>> from eigenscript.lexer import Tokenizer
        >>> from eigenscript.parser import Parser
        >>> source = "x is 5"
        >>> tokens = Tokenizer(source).tokenize()
        >>> ast = Parser(tokens).parse()
        >>> interpreter = Interpreter()
        >>> result = interpreter.evaluate(ast)
    """

    def __init__(
        self,
        dimension: int = 768,
        metric_type: str = "euclidean",
        max_iterations: Optional[int] = None,
        convergence_threshold: float = 0.95,
        enable_convergence_detection: bool = True,
    ):
        """
        Initialize the interpreter.

        Args:
            dimension: LRVM space dimensionality
            metric_type: Type of metric tensor to use
            max_iterations: Maximum loop iterations (None = unbounded for Turing completeness)
            convergence_threshold: FS threshold for eigenstate detection (default: 0.95)
            enable_convergence_detection: Enable automatic convergence detection (default: True)
        """
        # Geometric components
        self.space = LRVMSpace(dimension=dimension)
        self.metric = MetricTensor(dimension=dimension, metric_type=metric_type)

        # Runtime state
        self.environment = Environment()
        self.fs_tracker = FrameworkStrengthTracker()
        self.max_iterations = max_iterations

        # Convergence detection
        self.convergence_threshold = convergence_threshold
        self.enable_convergence_detection = enable_convergence_detection
        self.recursion_depth = 0
        self.max_recursion_depth = 1000  # Safety limit

        # Special lightlike OF vector
        self._of_vector = self._create_of_vector()

    def _create_of_vector(self) -> LRVMVector:
        """
        Create the special lightlike OF vector.

        The OF operator must have ||OF||² = 0 (null norm).

        Returns:
            Lightlike LRVM vector
        """
        # TODO: Properly construct lightlike vector for the chosen metric
        # For Minkowski metric, (1, 1, 0, ...) works
        # For Euclidean, we need a different approach

        if self.metric.metric_type == "minkowski":
            coords = np.zeros(self.space.dimension)
            coords[0] = 1.0  # Timelike component
            coords[1] = 1.0  # Spacelike component
            # Result: norm = -1 + 1 = 0 (lightlike)
        else:
            # For Euclidean metric, just use zero vector (placeholder)
            coords = np.zeros(self.space.dimension)

        return LRVMVector(coords)

    def evaluate(self, node: ASTNode) -> LRVMVector:
        """
        Evaluate an AST node to an LRVM vector.

        Dispatches to appropriate evaluation method based on node type.

        Args:
            node: AST node to evaluate

        Returns:
            LRVM vector result

        Raises:
            RuntimeError: If evaluation fails
        """
        if isinstance(node, Program):
            return self._eval_program(node)
        elif isinstance(node, Assignment):
            return self._eval_assignment(node)
        elif isinstance(node, Relation):
            return self._eval_relation(node)
        elif isinstance(node, BinaryOp):
            return self._eval_binary_op(node)
        elif isinstance(node, Conditional):
            return self._eval_conditional(node)
        elif isinstance(node, Loop):
            return self._eval_loop(node)
        elif isinstance(node, FunctionDef):
            return self._eval_function_def(node)
        elif isinstance(node, Return):
            return self._eval_return(node)
        elif isinstance(node, Literal):
            return self._eval_literal(node)
        elif isinstance(node, Identifier):
            return self._eval_identifier(node)
        else:
            raise RuntimeError(f"Unknown AST node type: {type(node).__name__}")

    def _eval_program(self, node: Program) -> LRVMVector:
        """Evaluate a program (sequence of statements)."""
        result = self.space.zero_vector()

        for statement in node.statements:
            result = self.evaluate(statement)
            # Update Framework Strength tracker
            self.fs_tracker.update(result)

        return result

    def _eval_assignment(self, node: Assignment) -> LRVMVector:
        """
        Evaluate IS operator: x is y

        Semantic: Projection/binding in LRVM space
        """
        # Evaluate right-hand side
        value = self.evaluate(node.expression)

        # Bind in environment
        self.environment.bind(node.identifier, value)

        return value

    def _eval_relation(self, node: Relation) -> LRVMVector:
        """
        Evaluate OF operator: x of y

        Semantic: Metric contraction x^T g y OR function application
        """
        # Special handling for function calls:
        # If left side is an identifier, check if it's a function before evaluating
        if isinstance(node.left, Identifier):
            try:
                left_value = self.environment.lookup(node.left.name)
                if isinstance(left_value, Function):
                    # This is a function call!
                    return self._call_function(left_value, node.right)
            except NameError:
                pass  # Not found, will evaluate normally below

        # Evaluate both sides normally
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        # Check if left is a function (in case it came from a complex expression)
        if isinstance(left, Function):
            # right should already be evaluated
            return self._call_function_with_value(left, right)

        # Special case: OF of OF = OF
        if self._is_of_vector(left) and self._is_of_vector(right):
            return self._of_vector

        # Perform metric contraction and return as vector
        return self.metric.contract_to_vector(left, right)

    def _eval_binary_op(self, node: "BinaryOp") -> LRVMVector:
        """
        Evaluate binary arithmetic operators (+, -, *, /, =, <, >).

        Semantic: Arithmetic operators as equilibrium operations:
            + = additive equilibrium (vector composition)
            - = subtractive equilibrium (directed distance)
            * = multiplicative equilibrium (radial scaling)
            / = projected multiplicative equilibrium (ratio)
            = = equality equilibrium (IS test)
            < = proximity to equilibrium test
            > = distance from equilibrium test
        """
        # Evaluate both operands
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == "+":
            # Addition: additive equilibrium composition
            # ‖a+b‖² = ‖a‖² + ‖b‖² + 2(a^T g b)
            return left.add(right)

        elif node.operator == "-":
            # Subtraction: additive equilibrium inversion
            # ‖a-b‖² = ‖a‖² + ‖b‖² - 2(a^T g b)
            return left.subtract(right)

        elif node.operator == "*":
            # Multiplication: multiplicative equilibrium scaling
            # Extract scalar from first coordinate and scale
            scalar = right.coords[0]
            return left.scale(scalar)

        elif node.operator == "/":
            # Division: projected multiplicative equilibrium
            # Project through inverse scaling
            scalar = right.coords[0]
            if abs(scalar) < 1e-10:
                raise RuntimeError("Division by zero (equilibrium singularity)")
            return left.scale(1.0 / scalar)

        elif node.operator == "=":
            # Equality: IS operator (equilibrium test)
            # Returns 1 if equal, 0 otherwise (as embedded scalar)
            is_equal = self.space.is_operator(left, right, self.metric.g)
            return self.space.embed_scalar(1.0 if is_equal else 0.0)

        elif node.operator == "<":
            # Less than: ordered equilibrium test
            # For scalars, compare first coordinate directly
            left_val = left.coords[0]
            right_val = right.coords[0]
            result = 1.0 if left_val < right_val else 0.0
            return self.space.embed_scalar(result)

        elif node.operator == ">":
            # Greater than: inverse ordered equilibrium test
            # For scalars, compare first coordinate directly
            left_val = left.coords[0]
            right_val = right.coords[0]
            result = 1.0 if left_val > right_val else 0.0
            return self.space.embed_scalar(result)

        else:
            raise RuntimeError(f"Unknown binary operator: {node.operator}")

    def _eval_conditional(self, node: Conditional) -> LRVMVector:
        """
        Evaluate IF statement.

        Semantic: Branch based on value
        - For boolean results (from comparisons): check coords[0] > 0
        - For other values: check norm > 0
        """
        # Evaluate condition
        condition = self.evaluate(node.condition)

        # Determine truthiness
        # For comparison results, use first coordinate (0.0 or 1.0)
        # For other values, use norm
        condition_value = condition.coords[0]

        # Branch based on condition value
        # True if first coordinate is non-zero (handles both boolean and norm cases)
        if abs(condition_value) > 1e-10:
            return self._eval_block(node.if_block)
        else:
            if node.else_block:
                return self._eval_block(node.else_block)
            else:
                return self.space.zero_vector()

    def _eval_loop(self, node: Loop) -> LRVMVector:
        """
        Evaluate LOOP statement.

        Semantic: Iterate until convergence in LRVM space.

        When max_iterations is None, loops can execute unbounded computation,
        achieving Turing completeness.
        """
        result = self.space.zero_vector()
        previous = None
        convergence_threshold = 1e-6
        iterations = 0

        while True:
            # Check iteration limit (if set)
            if self.max_iterations is not None and iterations >= self.max_iterations:
                break

            # Evaluate condition
            condition = self.evaluate(node.condition)

            # Exit if condition is "false" (first coordinate ≈ 0)
            # This handles both comparison operators and norm-based conditions
            condition_value = condition.coords[0]
            if abs(condition_value) < convergence_threshold:
                break

            # Execute loop body
            result = self._eval_block(node.body)

            # Check for convergence
            if previous is not None:
                distance = self.metric.distance(result, previous)
                if distance < convergence_threshold:
                    break

            previous = result
            iterations += 1

        return result

    def _eval_function_def(self, node: FunctionDef) -> LRVMVector:
        """
        Evaluate function definition.

        Semantic: Create timelike transformation
        """
        # Create function object with current environment as closure
        func = Function(
            name=node.name,
            parameters=node.parameters if node.parameters else ["n"],  # Default parameter name
            body=node.body,
            closure=self.environment
        )

        # Bind function in environment
        self.environment.bind(node.name, func)

        # Return a vector representation of the function (for geometric consistency)
        # Functions have timelike signature (negative norm)
        func_vector = self.space.embed_string(f"<function {node.name}>")
        return func_vector

    def _eval_return(self, node: Return) -> LRVMVector:
        """
        Evaluate return statement.

        Semantic: Project onto observer frame

        Raises:
            ReturnValue: To unwind the stack and return from function
        """
        value = self.evaluate(node.expression)
        raise ReturnValue(value)

    def _eval_literal(self, node: Literal) -> LRVMVector:
        """
        Evaluate a literal value.

        Convert literal to LRVM vector using appropriate embedding.
        """
        if node.literal_type == "number":
            return self.space.embed_scalar(float(node.value))
        elif node.literal_type == "string":
            return self.space.embed_string(node.value)
        elif node.literal_type == "null":
            return self.space.zero_vector()
        elif node.literal_type == "vector":
            # node.value should be a list of numbers
            return LRVMVector(node.value)
        else:
            raise RuntimeError(f"Unknown literal type: {node.literal_type}")

    def _eval_identifier(self, node: Identifier) -> LRVMVector:
        """
        Evaluate an identifier (variable lookup).
        """
        # Special case: OF is the lightlike operator
        if node.name.upper() == "OF":
            return self._of_vector

        return self.environment.lookup(node.name)

    def _eval_block(self, statements: list[ASTNode]) -> LRVMVector:
        """
        Evaluate a block of statements.

        Returns the value of the last statement.
        """
        result = self.space.zero_vector()

        for statement in statements:
            result = self.evaluate(statement)

        return result

    def _call_function(self, func: Function, arg_node: ASTNode) -> LRVMVector:
        """
        Call a function with an unevaluated argument expression.

        Args:
            func: Function object to call
            arg_node: AST node for the argument (will be evaluated)

        Returns:
            Result of function execution
        """
        # Evaluate the argument
        arg_value = self.evaluate(arg_node)
        return self._call_function_with_value(func, arg_value)

    def _call_function_with_value(self, func: Function, arg_value: LRVMVector) -> LRVMVector:
        """
        Call a function with an already-evaluated argument.

        Implements convergence detection: if FS > threshold during recursion,
        return current eigenstate instead of continuing.

        Args:
            func: Function object to call
            arg_value: Evaluated argument value

        Returns:
            Result of function execution or eigenstate if converged
        """
        # Track recursion depth
        self.recursion_depth += 1

        # Safety check: prevent infinite recursion
        if self.recursion_depth > self.max_recursion_depth:
            self.recursion_depth -= 1
            raise RuntimeError(
                f"Maximum recursion depth ({self.max_recursion_depth}) exceeded. "
                "System may be diverging."
            )

        # Convergence detection: check if we've reached eigenstate
        if self.enable_convergence_detection and self.recursion_depth > 2:
            # Update FS tracker with current argument value to build trajectory
            self.fs_tracker.update(arg_value)

            fs = self.fs_tracker.compute_fs()

            # Detect convergence via multiple criteria (inspired by EigenFunction):
            # 1. High Framework Strength (FS > threshold)
            # 2. Fixed-point loop detection (low variance)
            # 3. Oscillation pattern detection (paradox/divergence indicator)
            converged = False
            variance = 0.0
            oscillation_score = 0.0

            if fs >= self.convergence_threshold:
                converged = True
            elif self.recursion_depth > 5:  # Deep enough to detect patterns
                trajectory_len = self.fs_tracker.get_trajectory_length()
                if trajectory_len >= 3:
                    # Check variance of recent states to detect cycles
                    recent_states = self.fs_tracker.trajectory[-3:]
                    coords = np.array([s.coords for s in recent_states])
                    variance = float(np.var(coords))

                    # Low variance indicates a fixed-point or cycle
                    if variance < 1e-6:
                        converged = True

                # Oscillation detection (EigenFunction-inspired)
                # Track sign changes in coordinate deltas to detect paradoxical loops
                if trajectory_len >= 5:
                    # Compute deltas from first coordinate of trajectory
                    values = [state.coords[0] for state in self.fs_tracker.trajectory[-5:]]
                    deltas = np.diff(values)

                    if len(deltas) > 1:
                        # Count sign changes (oscillation indicator)
                        sign_changes = np.sum(np.diff(np.sign(deltas)) != 0)
                        oscillation_score = sign_changes / len(deltas)

                        # High oscillation (> 0.15) suggests divergence/paradox
                        # In this case, force convergence to eigenstate
                        if oscillation_score > 0.15:
                            converged = True

            if converged:
                # Eigenstate convergence detected!
                self.recursion_depth -= 1

                # Create eigenstate marker vector with diagnostic info
                eigenstate_str = f"<eigenstate FS={fs:.4f} var={variance:.6f} osc={oscillation_score:.3f} depth={self.recursion_depth}>"
                eigenstate = self.space.embed_string(eigenstate_str)
                return eigenstate

        # Create new environment for function execution
        # Parent is the function's closure (lexical scoping)
        func_env = Environment(parent=func.closure)

        # Bind arguments to parameters
        # For now, we support single-argument functions with implicit parameter 'n'
        if func.parameters:
            param_name = func.parameters[0]
        else:
            param_name = "n"  # Default parameter name

        func_env.bind(param_name, arg_value)

        # Execute function body
        # Save current environment and switch to function environment
        saved_env = self.environment
        self.environment = func_env

        try:
            result = self.space.zero_vector()

            # Execute each statement in function body
            for statement in func.body:
                result = self.evaluate(statement)
                # Update Framework Strength tracker during execution
                self.fs_tracker.update(result)

            return result

        except ReturnValue as ret:
            # Return statement was executed
            # Update FS with return value
            self.fs_tracker.update(ret.value)
            return ret.value

        finally:
            # Restore original environment and decrement recursion depth
            self.environment = saved_env
            self.recursion_depth -= 1

    def _is_of_vector(self, vector: LRVMVector) -> bool:
        """
        Check if a vector is the special OF vector.
        """
        return self.metric.is_lightlike(vector)

    def get_framework_strength(self) -> float:
        """
        Get current Framework Strength.

        Returns:
            FS value between 0.0 and 1.0
        """
        return self.fs_tracker.compute_fs()

    def has_converged(self, threshold: float = 0.95) -> bool:
        """
        Check if execution has reached eigenstate convergence.

        Args:
            threshold: FS threshold for convergence

        Returns:
            True if FS >= threshold
        """
        return self.fs_tracker.has_converged(threshold)
