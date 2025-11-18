"""
Unified Interpreter for EigenScript v2.0

This interpreter implements the fundamental insight:
    OF is the projection of IS through the metric tensor g.

Key principles:
1. IS = symmetric identity relation (||x - y||² = 0)
2. OF = projected identity (x^T g y = π_g(IS))
3. AND = vector addition (x + y)

All computation reduces to these three geometric operations.
"""

import numpy as np
from typing import Dict, Optional, Any, Callable
from eigenscript.parser.ast_builder import *
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.semantic.metric import MetricTensor
from eigenscript.semantic.operations import GeometricOperations
from eigenscript.runtime.framework_strength import FrameworkStrengthTracker


class UnifiedEnvironment:
    """
    Environment for variable bindings.

    In EigenScript, bindings are created via IS (identity relation).
    """

    def __init__(self, parent: Optional["UnifiedEnvironment"] = None):
        """
        Initialize environment.

        Args:
            parent: Parent environment for nested scopes
        """
        self.bindings: Dict[str, LRVMVector] = {}
        self.parent = parent

    def bind_is(self, name: str, vector: LRVMVector) -> None:
        """
        Bind a variable via IS (identity relation).

        This creates the identity: name IS vector

        Args:
            name: Variable name
            vector: LRVM vector value
        """
        self.bindings[name] = vector

    def lookup(self, name: str) -> LRVMVector:
        """
        Resolve a variable to its LRVM vector.

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
        return f"UnifiedEnvironment({len(self.bindings)} bindings)"


class UnifiedInterpreter:
    """
    Unified interpreter implementing the geometric operator theory.

    Core Principle:
        OF = π_g(IS)

    All operations reduce to:
        - IS (identity)
        - OF (projected identity)
        - AND (addition)
    """

    def __init__(
        self,
        dimension: int = 768,
        metric_type: str = "euclidean"
    ):
        """
        Initialize the unified interpreter.

        Args:
            dimension: LRVM space dimensionality
            metric_type: Type of metric tensor
        """
        # Geometric infrastructure
        self.space = LRVMSpace(dimension=dimension)
        self.metric = MetricTensor(dimension=dimension, metric_type=metric_type)
        self.ops = GeometricOperations(self.metric)

        # Runtime state
        self.environment = UnifiedEnvironment()
        self.fs_tracker = FrameworkStrengthTracker()

        # Special vectors
        self._of_vector = self._create_of_vector()
        self._null_vector = self.space.zero_vector()

    def _create_of_vector(self) -> LRVMVector:
        """
        Create the special OF operator vector.

        The OF operator must be lightlike: ||OF||² = 0

        Returns:
            Lightlike LRVM vector representing OF
        """
        if self.metric.metric_type == "minkowski":
            # In Minkowski space: (1, 1, 0, ...) is lightlike
            coords = np.zeros(self.space.dimension)
            coords[0] = 1.0  # Timelike component
            coords[1] = 1.0  # Spacelike component
            # norm = -1 + 1 = 0 (lightlike!)
        else:
            # For Euclidean, use zero vector (placeholder)
            coords = np.zeros(self.space.dimension)

        return LRVMVector(coords)

    # ========================================================================
    # Main Evaluation
    # ========================================================================

    def evaluate(self, node: ASTNode) -> LRVMVector:
        """
        Evaluate an AST node to an LRVM vector.

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

    # ========================================================================
    # IS Operator - Symmetric Identity
    # ========================================================================

    def _eval_assignment(self, node: Assignment) -> LRVMVector:
        """
        Evaluate IS operator: x is y

        Semantic: Create identity relation
            is(x, y) ⟺ ||x - y||² = 0

        Implementation:
            1. Evaluate right-hand side to get vector
            2. Bind identifier to that vector (force identity)
            3. Return the vector

        Args:
            node: Assignment AST node

        Returns:
            The bound vector
        """
        # Evaluate right-hand side
        value = self.evaluate(node.expression)

        # Create identity binding (IS operation)
        self.environment.bind_is(node.identifier, value)

        # Update Framework Strength
        self.fs_tracker.update(value)

        return value

    # ========================================================================
    # OF Operator - Projected Identity
    # ========================================================================

    def _eval_relation(self, node: Relation) -> LRVMVector:
        """
        Evaluate OF operator: x of y

        Semantic: Projected identity through metric g
            of(x, y) = x^T g y = π_g(is(x, y))

        Special cases:
            - OF of OF = OF (fixed point)
            - ||of(x, y)||² = 0  ⟺  is(x, y)

        Args:
            node: Relation AST node

        Returns:
            Result of metric contraction
        """
        # Evaluate both sides
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        # Special case: OF of OF = OF (fixed point)
        if self._is_of_vector(left) and self._is_of_vector(right):
            return self._of_vector

        # General case: Metric contraction (projection of identity)
        result = self.ops.of_relation(left, right)

        # Check if OF collapsed to IS (lightlike result)
        if self.ops.of_collapses_to_is(left, right):
            # OF has collapsed to IS - they're identical!
            # This is the boundary where OF → IS
            pass

        return result

    # ========================================================================
    # AND Operator - Vector Addition
    # ========================================================================

    def _eval_and(self, left: ASTNode, right: ASTNode) -> LRVMVector:
        """
        Evaluate AND operator: x and y

        Semantic: Vector addition in LRVM space
            and(x, y) = x + y

        Args:
            left: Left operand AST node
            right: Right operand AST node

        Returns:
            Sum vector
        """
        left_vec = self.evaluate(left)
        right_vec = self.evaluate(right)

        return self.ops.and_combine(left_vec, right_vec)

    # ========================================================================
    # Control Flow
    # ========================================================================

    def _eval_conditional(self, node: Conditional) -> LRVMVector:
        """
        Evaluate IF statement (geometric conditional).

        Semantic: Branch based on norm signature
            ||condition||² > 0  → spacelike/timelike → if branch
            ||condition||² ≈ 0  → lightlike → else branch

        Args:
            node: Conditional AST node

        Returns:
            Result of executed branch
        """
        # Evaluate condition
        condition = self.evaluate(node.condition)

        # Compute norm signature
        norm = self.metric.norm(condition)

        # Branch based on geometry
        if norm > 0:  # Spacelike/timelike → meaningful
            return self._eval_block(node.if_block)
        else:  # Lightlike → boundary case
            if node.else_block:
                return self._eval_block(node.else_block)
            else:
                return self._null_vector

    def _eval_loop(self, node: Loop) -> LRVMVector:
        """
        Evaluate LOOP statement (geodesic iteration).

        Semantic: Iterate until convergence
            - Stop when ||condition||² → 0 (lightlike)
            - Stop when state converges
            - Stop when Framework Strength → 1.0

        Args:
            node: Loop AST node

        Returns:
            Final state vector
        """
        result = self._null_vector
        previous = None
        convergence_threshold = 1e-6
        max_iterations = 10000
        iterations = 0

        while iterations < max_iterations:
            # Evaluate condition
            condition = self.evaluate(node.condition)
            norm = self.metric.norm(condition)

            # Exit if condition is lightlike (collapsed to identity)
            if abs(norm) < convergence_threshold:
                break

            # Execute loop body
            result = self._eval_block(node.body)

            # Check for state convergence (OF → IS)
            if previous is not None:
                # Check if of(result, previous) has collapsed to IS
                if self.ops.of_collapses_to_is(result, previous):
                    # Eigenstate reached!
                    break

            # Check Framework Strength convergence
            self.fs_tracker.update(result)
            if self.fs_tracker.has_converged(threshold=0.99):
                # Understanding achieved!
                break

            previous = result
            iterations += 1

        return result

    # ========================================================================
    # Primitives
    # ========================================================================

    def _eval_literal(self, node: Literal) -> LRVMVector:
        """
        Evaluate a literal value.

        Maps literals to LRVM vectors via embedding.

        Args:
            node: Literal AST node

        Returns:
            LRVM vector representation
        """
        if node.literal_type == "number":
            return self.space.embed_scalar(float(node.value))
        elif node.literal_type == "string":
            return self.space.embed_string(node.value)
        elif node.literal_type == "null":
            return self._null_vector
        elif node.literal_type == "vector":
            # node.value should be a list of numbers
            # Pad or truncate to match space dimension
            coords = np.zeros(self.space.dimension)
            for i, val in enumerate(node.value[:self.space.dimension]):
                coords[i] = float(val)
            return LRVMVector(coords)
        else:
            raise RuntimeError(f"Unknown literal type: {node.literal_type}")

    def _eval_identifier(self, node: Identifier) -> LRVMVector:
        """
        Evaluate an identifier (variable lookup).

        Args:
            node: Identifier AST node

        Returns:
            LRVM vector bound to the identifier
        """
        # Special case: OF is the lightlike operator
        if node.name.upper() == "OF":
            return self._of_vector

        return self.environment.lookup(node.name)

    def _eval_program(self, node: Program) -> LRVMVector:
        """
        Evaluate a program (sequence of statements).

        Args:
            node: Program AST node

        Returns:
            Result of last statement
        """
        result = self._null_vector

        for statement in node.statements:
            result = self.evaluate(statement)
            self.fs_tracker.update(result)

        return result

    def _eval_block(self, statements: list[ASTNode]) -> LRVMVector:
        """
        Evaluate a block of statements.

        Args:
            statements: List of AST nodes

        Returns:
            Result of last statement
        """
        result = self._null_vector

        for statement in statements:
            result = self.evaluate(statement)

        return result

    def _eval_function_def(self, node: FunctionDef) -> LRVMVector:
        """
        Evaluate function definition.

        Creates a timelike transformation in LRVM space.

        Args:
            node: FunctionDef AST node

        Returns:
            Function vector (timelike)
        """
        # TODO: Implement proper function objects
        # For now, create placeholder timelike vector
        func_vector = self.space.random_vector()

        # Bind function name
        self.environment.bind_is(node.name, func_vector)

        return func_vector

    def _eval_return(self, node: Return) -> LRVMVector:
        """
        Evaluate return statement.

        Projects result onto observer frame.

        Args:
            node: Return AST node

        Returns:
            Return value vector
        """
        return self.evaluate(node.expression)

    # ========================================================================
    # Helpers
    # ========================================================================

    def _is_of_vector(self, vector: LRVMVector) -> bool:
        """
        Check if a vector is the special OF operator.

        Args:
            vector: LRVM vector to test

        Returns:
            True if this is the OF operator
        """
        return self.metric.is_lightlike(vector)

    # ========================================================================
    # Public API
    # ========================================================================

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

    def demonstrate_is_of_relationship(self, x: LRVMVector, y: LRVMVector) -> dict:
        """
        Demonstrate the fundamental IS/OF relationship.

        Shows that OF = π_g(IS) and that OF → IS when norm → 0.

        Args:
            x: First vector
            y: Second vector

        Returns:
            Dictionary with relationship information
        """
        # Check IS (identity relation)
        is_identical = self.ops.is_identical(x, y)

        # Compute OF (projected identity)
        of_result = self.ops.of_relation(x, y)
        of_norm = self.metric.norm(of_result)

        # Check if OF collapsed to IS
        of_is_lightlike = self.ops.of_collapses_to_is(x, y)

        # Symmetry tests
        is_symmetric = self.ops.is_is_symmetric(x, y)
        of_symmetric = self.ops.is_of_symmetric(x, y)

        return {
            "is_identical": is_identical,
            "of_result_norm": of_norm,
            "of_collapsed_to_is": of_is_lightlike,
            "is_is_symmetric": is_symmetric,
            "of_is_symmetric": of_symmetric,
            "interpretation": self._interpret_relationship(
                is_identical, of_norm, of_is_lightlike
            )
        }

    def _interpret_relationship(
        self,
        is_identical: bool,
        of_norm: float,
        of_collapsed: bool
    ) -> str:
        """
        Interpret the IS/OF relationship.

        Args:
            is_identical: Whether IS relation holds
            of_norm: Norm of OF projection
            of_collapsed: Whether OF collapsed to IS

        Returns:
            Human-readable interpretation
        """
        if is_identical and of_collapsed:
            return "IS and OF agree: Perfect identity (lightlike)"
        elif of_collapsed:
            return "OF collapsed to IS: Eigenstate reached"
        elif abs(of_norm) < 1e-6:
            return "Near-identity: OF approaching IS"
        elif of_norm > 0:
            return "Spacelike relation: Distinct entities"
        else:
            return "Timelike relation: Causal/functional"

    def __repr__(self) -> str:
        """String representation."""
        fs = self.get_framework_strength()
        return (
            f"UnifiedInterpreter("
            f"dim={self.space.dimension}, "
            f"metric={self.metric.metric_type}, "
            f"FS={fs:.3f})"
        )
