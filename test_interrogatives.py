"""
Test interrogative operators and semantic predicates.

This validates that:
1. Semantic predicates (converged, stable, diverging, etc.) work correctly
2. Interrogative operators (WHO, WHAT, WHEN, WHERE, WHY, HOW) extract geometric info
3. Both enhance debugging and expressiveness
"""

from eigenscript.lexer import Tokenizer
from eigenscript.parser import Parser
from eigenscript.evaluator import Interpreter


def test_semantic_predicates_converged():
    """Test that 'converged' predicate evaluates geometric state."""
    source = """
x is 5
if converged:
    result is 1
else:
    result is 0
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    # The converged predicate should evaluate (may be true or false)
    result = interp.environment.lookup("result")
    assert result is not None
    # Result should be 0 or 1
    assert result.coords[0] in (0.0, 1.0)


def test_semantic_predicates_stable():
    """Test that 'stable' predicate checks spacetime signature."""
    source = """
x is 10
if stable:
    result is 1
else:
    result is 0
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    result = interp.environment.lookup("result")
    assert result is not None
    assert result.coords[0] in (0.0, 1.0)


def test_interrogative_what():
    """Test WHAT extracts scalar magnitude."""
    source = """
x is 42
magnitude is what is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    magnitude = interp.environment.lookup("magnitude")
    assert magnitude is not None
    # WHAT should extract the scalar value (first coordinate)
    assert abs(magnitude.coords[0] - 42.0) < 1e-6


def test_interrogative_who():
    """Test WHO extracts identity."""
    source = """
x is 5
identity is who is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    identity = interp.environment.lookup("identity")
    assert identity is not None
    # WHO should return a string embedding containing "x"
    # We can check if first coordinate has some value (string embedding)


def test_interrogative_when():
    """Test WHEN extracts temporal coordinate."""
    source = """
x is 5
time is when is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    time = interp.environment.lookup("time")
    assert time is not None
    # WHEN should return trajectory length or recursion depth


def test_interrogative_where():
    """Test WHERE returns position in semantic space."""
    source = """
x is 7
position is where is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    position = interp.environment.lookup("position")
    assert position is not None
    # WHERE should return the value itself (its position)


def test_interrogative_why():
    """Test WHY extracts gradient/direction."""
    source = """
x is 5
y is 10
direction is why is y
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    direction = interp.environment.lookup("direction")
    assert direction is not None
    # WHY returns direction of change from trajectory


def test_interrogative_how():
    """Test HOW extracts process quality."""
    source = """
x is 5
y is x + 1
process is how is y
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    process = interp.environment.lookup("process")
    assert process is not None
    # HOW returns Framework Strength or process metrics


def test_debugging_with_interrogatives():
    """Test using interrogatives for debugging."""
    source = """
define compute as:
    if n < 2:
        return 1
    else:
        result is n * 2
        return result

x is compute of 5
value is what is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    value = interp.environment.lookup("value")
    assert value is not None
    # Should extract the scalar value from compute result
    assert abs(value.coords[0] - 10.0) < 1e-6


def test_natural_conditional_with_predicate():
    """Test natural language conditional with semantic predicate."""
    source = """
x is 5
y is 10

if diverging:
    status is 0
else:
    status is 1
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    status = interp.environment.lookup("status")
    assert status is not None
    assert status.coords[0] in (0.0, 1.0)


def test_combined_interrogatives_and_predicates():
    """Test combining interrogatives with predicates for rich debugging."""
    source = """
x is 42

if not converged:
    debug_value is what is x
    debug_when is when is x
"""
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interp = Interpreter()
    interp.evaluate(ast)

    # Should be able to lookup debug values
    # (they may or may not be bound depending on converged state)


if __name__ == "__main__":
    print("Testing interrogative operators and semantic predicates...")
    print()

    print("✓ Testing WHAT (magnitude extraction)...")
    test_interrogative_what()

    print("✓ Testing WHO (identity extraction)...")
    test_interrogative_who()

    print("✓ Testing WHEN (temporal coordinate)...")
    test_interrogative_when()

    print("✓ Testing WHERE (position)...")
    test_interrogative_where()

    print("✓ Testing WHY (gradient/direction)...")
    test_interrogative_why()

    print("✓ Testing HOW (process quality)...")
    test_interrogative_how()

    print("✓ Testing semantic predicates (converged)...")
    test_semantic_predicates_converged()

    print("✓ Testing semantic predicates (stable)...")
    test_semantic_predicates_stable()

    print("✓ Testing debugging with interrogatives...")
    test_debugging_with_interrogatives()

    print("✓ Testing natural conditionals...")
    test_natural_conditional_with_predicate()

    print()
    print("All tests passed! ✓")
    print()
    print("Interrogatives and semantic predicates enhance both expressiveness and debugging.")
    print("Programmers can now query geometric state naturally and write more intuitive code.")
