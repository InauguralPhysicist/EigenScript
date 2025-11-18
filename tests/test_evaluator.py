"""
Unit tests for the EigenScript evaluator/interpreter.

Tests execution of AST nodes and geometric transformations.
"""

import pytest
import numpy as np
from eigenscript.evaluator import Interpreter, Environment
from eigenscript.parser.ast_builder import *
from eigenscript.semantic.lrvm import LRVMVector


class TestEnvironment:
    """Test suite for Environment class."""

    def test_environment_creation(self):
        """Should create empty environment."""
        env = Environment()
        assert len(env.bindings) == 0
        assert env.parent is None

    def test_bind_and_lookup(self):
        """Should bind and lookup variables."""
        env = Environment()
        v = LRVMVector([1.0, 2.0, 3.0])

        env.bind("x", v)
        result = env.lookup("x")

        assert result == v

    def test_lookup_undefined_variable(self):
        """Lookup of undefined variable should raise NameError."""
        env = Environment()

        with pytest.raises(NameError):
            env.lookup("undefined")

    def test_parent_environment(self):
        """Should lookup in parent if not found locally."""
        parent = Environment()
        child = Environment(parent=parent)

        v = LRVMVector([1.0, 2.0, 3.0])
        parent.bind("x", v)

        # Child should find x in parent
        result = child.lookup("x")
        assert result == v

    def test_shadowing(self):
        """Child binding should shadow parent."""
        parent = Environment()
        child = Environment(parent=parent)

        v1 = LRVMVector([1.0, 0.0, 0.0])
        v2 = LRVMVector([2.0, 0.0, 0.0])

        parent.bind("x", v1)
        child.bind("x", v2)

        # Child lookup should get child's binding
        assert child.lookup("x") == v2
        # Parent lookup should still get parent's binding
        assert parent.lookup("x") == v1


class TestInterpreter:
    """Test suite for Interpreter class."""

    def test_interpreter_creation(self):
        """Should create interpreter with default settings."""
        interp = Interpreter()
        assert interp.space.dimension == 768
        assert interp.metric.dimension == 768

    def test_interpreter_custom_dimension(self):
        """Should create interpreter with custom dimension."""
        interp = Interpreter(dimension=100)
        assert interp.space.dimension == 100
        assert interp.metric.dimension == 100

    def test_eval_literal_number(self):
        """Should evaluate number literal."""
        interp = Interpreter(dimension=10)
        lit = Literal(value=5.0, literal_type="number")

        result = interp.evaluate(lit)

        assert isinstance(result, LRVMVector)
        assert result.dimension == 10

    def test_eval_literal_string(self):
        """Should evaluate string literal."""
        interp = Interpreter(dimension=10)
        lit = Literal(value="hello", literal_type="string")

        result = interp.evaluate(lit)

        assert isinstance(result, LRVMVector)
        assert result.dimension == 10

    def test_eval_literal_null(self):
        """Should evaluate null literal as zero vector."""
        interp = Interpreter(dimension=10)
        lit = Literal(value=None, literal_type="null")

        result = interp.evaluate(lit)

        assert isinstance(result, LRVMVector)
        assert np.allclose(result.coords, np.zeros(10))

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_assignment(self):
        """Should evaluate assignment and bind variable."""
        interp = Interpreter(dimension=10)

        # x is 5
        assign = Assignment(
            identifier="x", expression=Literal(value=5.0, literal_type="number")
        )

        interp.evaluate(assign)

        # x should now be bound in environment
        result = interp.environment.lookup("x")
        assert isinstance(result, LRVMVector)

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_identifier(self):
        """Should evaluate identifier to bound value."""
        interp = Interpreter(dimension=10)

        # Bind x first
        v = LRVMVector(np.ones(10))
        interp.environment.bind("x", v)

        # Evaluate identifier
        ident = Identifier(name="x")
        result = interp.evaluate(ident)

        assert result == v

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_relation(self):
        """Should evaluate OF operator via metric contraction."""
        interp = Interpreter(dimension=5)

        # Bind x and y
        x = LRVMVector([1.0, 0.0, 0.0, 0.0, 0.0])
        y = LRVMVector([2.0, 0.0, 0.0, 0.0, 0.0])
        interp.environment.bind("x", x)
        interp.environment.bind("y", y)

        # x of y
        rel = Relation(left=Identifier("x"), right=Identifier("y"))
        result = interp.evaluate(rel)

        # Result should be contraction: x^T g y = 1*2 = 2
        assert isinstance(result, LRVMVector)
        # First coordinate should have contraction value
        assert np.isclose(result.coords[0], 2.0)

    @pytest.mark.skip(reason="Full implementation pending")
    def test_of_of_equals_of(self):
        """Should verify OF of OF = OF property."""
        # This is a key property of EigenScript
        # The OF operator applied to itself should return itself
        pass

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_conditional_true_branch(self):
        """Should evaluate true branch when condition is spacelike."""
        pass

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_conditional_false_branch(self):
        """Should evaluate false branch when condition is lightlike."""
        pass

    @pytest.mark.skip(reason="Full implementation pending")
    def test_eval_loop_convergence(self):
        """Should iterate until convergence."""
        pass

    def test_framework_strength_tracking(self):
        """Should track Framework Strength during execution."""
        interp = Interpreter(dimension=10)

        # Execute some operations
        lit1 = Literal(value=1.0, literal_type="number")
        lit2 = Literal(value=2.0, literal_type="number")

        interp.evaluate(lit1)
        interp.evaluate(lit2)

        # Should be able to get FS
        fs = interp.get_framework_strength()
        assert isinstance(fs, float)
        assert 0.0 <= fs <= 1.0

    def test_convergence_detection(self):
        """Should detect eigenstate convergence."""
        interp = Interpreter(dimension=10)

        # Initially should not be converged
        assert not interp.has_converged(threshold=0.95)


class TestEndToEnd:
    """End-to-end integration tests."""

    @pytest.mark.skip(reason="Full implementation pending")
    def test_simple_program(self):
        """Should execute simple program: x is 5"""
        # This would test the full pipeline:
        # Source → Lexer → Parser → Evaluator
        pass

    @pytest.mark.skip(reason="Full implementation pending")
    def test_relation_program(self):
        """Should execute: z is x of y"""
        pass

    @pytest.mark.skip(reason="Full implementation pending")
    def test_self_reference(self):
        """Should handle self-reference safely."""
        # observer of observer should converge, not explode
        pass
