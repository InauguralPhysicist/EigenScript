"""
Interpreter for EigenScript.

Executes Abstract Syntax Trees using geometric transformations
in LRVM space.
"""

from typing import Dict, Optional, Any
from eigenscript.parser.ast_builder import *
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.semantic.metric import MetricTensor
from eigenscript.runtime.framework_strength import FrameworkStrengthTracker


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
        self.bindings: Dict[str, LRVMVector] = {}
        self.parent = parent

    def bind(self, name: str, vector: LRVMVector) -> None:
        """
        Create an immutable binding.

        In EigenScript, bindings are immutable - each IS creates
        a new point in semantic spacetime rather than mutating.

        Args:
            name: Variable name
            vector: LRVM vector value
        """
        self.bindings[name] = vector

    def lookup(self, name: str) -> LRVMVector:
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

    def __init__(self, dimension: int = 768, metric_type: str = "euclidean"):
        """
        Initialize the interpreter.

        Args:
            dimension: LRVM space dimensionality
            metric_type: Type of metric tensor to use
        """
        # Geometric components
        self.space = LRVMSpace(dimension=dimension)
        self.metric = MetricTensor(dimension=dimension, metric_type=metric_type)

        # Runtime state
        self.environment = Environment()
        self.fs_tracker = FrameworkStrengthTracker()

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

        Semantic: Metric contraction x^T g y
        """
        # Evaluate both sides
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        # Special case: OF of OF = OF
        if self._is_of_vector(left) and self._is_of_vector(right):
            return self._of_vector

        # Perform metric contraction and return as vector
        return self.metric.contract_to_vector(left, right)

    def _eval_conditional(self, node: Conditional) -> LRVMVector:
        """
        Evaluate IF statement.

        Semantic: Branch based on norm signature
        - norm > 0 (spacelike/meaningful) → if branch
        - norm ≈ 0 (lightlike/boundary) → else branch
        """
        # Evaluate condition
        condition = self.evaluate(node.condition)

        # Compute norm
        norm = self.metric.norm(condition)

        # Branch based on norm signature
        if norm > 0:  # Spacelike/Timelike → meaningful
            return self._eval_block(node.if_block)
        else:  # Lightlike → boundary case
            if node.else_block:
                return self._eval_block(node.else_block)
            else:
                return self.space.zero_vector()

    def _eval_loop(self, node: Loop) -> LRVMVector:
        """
        Evaluate LOOP statement.

        Semantic: Iterate until convergence in LRVM space
        """
        result = self.space.zero_vector()
        previous = None
        convergence_threshold = 1e-6
        max_iterations = 10000
        iterations = 0

        while iterations < max_iterations:
            # Evaluate condition
            condition = self.evaluate(node.condition)
            norm = self.metric.norm(condition)

            # Exit if condition is lightlike (boundary)
            if abs(norm) < convergence_threshold:
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
        # TODO: Implement function objects
        # For now, store in environment as a special vector
        func_vector = self.space.random_vector()  # Placeholder

        self.environment.bind(node.name, func_vector)
        return func_vector

    def _eval_return(self, node: Return) -> LRVMVector:
        """
        Evaluate return statement.

        Semantic: Project onto observer frame
        """
        return self.evaluate(node.expression)

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
