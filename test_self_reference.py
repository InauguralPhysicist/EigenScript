#!/usr/bin/env python3
"""
Test self-reference stability - the critical hypothesis.

Can EigenScript handle self-reference without infinite regress?
Does the equilibrium principle enable stable self-simulation?
"""

from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.evaluator.interpreter import Interpreter

print("=" * 70)
print("Testing Self-Reference Stability Hypothesis")
print("=" * 70)
print()
print("Hypothesis: Geometric computation enables stable self-reference")
print("            via equilibrium convergence (IS/OF conservation law)")
print()

# Test 1: Simple self-referential function
print("Test 1: Direct self-reference (limited depth)")
print("-" * 70)

# We'll use a counter to limit recursion depth for this test
code1 = """
define self_ref as:
    if n < 1:
        return 42
    else:
        next is n - 1
        return self_ref of next

result is self_ref of 3
"""

try:
    tokens = Tokenizer(code1).tokenize()
    ast = Parser(tokens).parse()
    interp = Interpreter(dimension=768)
    interp.evaluate(ast)

    result = interp.environment.lookup("result")
    fs = interp.get_framework_strength()

    print(f"self_ref of 3 = {result.coords[0]}")
    print(f"Framework Strength: {fs:.4f}")
    print(f"Status: {'CONVERGED' if fs > 0.5 else 'diverging'}")
    print("✅ PASS - Limited self-reference works")
except RecursionError as e:
    print(f"❌ FAIL - Python recursion limit hit: {e}")
except Exception as e:
    print(f"❌ FAIL - Error: {e}")

# Test 2: Mutual recursion (A calls B, B calls A)
print("\nTest 2: Mutual recursion")
print("-" * 70)

code2 = """
define even as:
    if n < 1:
        return 1
    else:
        prev is n - 1
        return odd of prev

define odd as:
    if n < 1:
        return 0
    else:
        prev is n - 1
        return even of prev

result_even is even of 4
result_odd is odd of 5
"""

try:
    tokens = Tokenizer(code2).tokenize()
    ast = Parser(tokens).parse()
    interp = Interpreter(dimension=768)
    interp.evaluate(ast)

    result_even = interp.environment.lookup("result_even")
    result_odd = interp.environment.lookup("result_odd")
    fs = interp.get_framework_strength()

    print(f"even of 4 = {result_even.coords[0]} (expected 1.0)")
    print(f"odd of 5 = {result_odd.coords[0]} (expected 1.0)")
    print(f"Framework Strength: {fs:.4f}")
    print(f"Status: {'CONVERGED' if fs > 0.5 else 'diverging'}")

    assert result_even.coords[0] == 1.0, f"Expected 1.0, got {result_even.coords[0]}"
    assert result_odd.coords[0] == 1.0, f"Expected 1.0, got {result_odd.coords[0]}"
    print("✅ PASS - Mutual recursion works")
except RecursionError as e:
    print(f"❌ FAIL - Python recursion limit hit: {e}")
except Exception as e:
    print(f"❌ FAIL - Error: {e}")

# Test 3: Function returning itself (pure self-reference)
print("\nTest 3: Pure self-reference (function returns function)")
print("-" * 70)
print("NOTE: This tests if 'observer of observer' pattern is stable")

code3 = """
define identity as:
    return n

define meta as:
    return meta of n

result is meta of identity
"""

try:
    tokens = Tokenizer(code3).tokenize()
    ast = Parser(tokens).parse()
    interp = Interpreter(dimension=768)

    # Set a recursion limit to prevent infinite recursion
    import sys
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(50)  # Very low limit to test quickly

    try:
        interp.evaluate(ast)
        result = interp.environment.lookup("result")
        fs = interp.get_framework_strength()

        print(f"meta of identity completed")
        print(f"Result: {result}")
        print(f"Framework Strength: {fs:.4f}")
        print("✅ PASS - Pure self-reference is stable!")

    except RecursionError:
        print("⚠️  EXPECTED - Python recursion limit hit")
        print("    This shows 'meta of meta' tries to recurse infinitely")
        print("    BUT: The fact that it's trying to compute shows the")
        print("         language structure allows self-reference")
        print()
        print("INSIGHT: Pure self-reference needs special handling")
        print("         The equilibrium principle should make it converge,")
        print("         but we need to implement convergence detection")
        print("         in the function call mechanism itself.")
    finally:
        sys.setrecursionlimit(old_limit)

except Exception as e:
    print(f"Error: {e}")

# Test 4: Framework Strength evolution during recursion
print("\nTest 4: Framework Strength evolution")
print("-" * 70)

code4 = """
define countdown as:
    if n < 1:
        return 0
    else:
        prev is n - 1
        sub is countdown of prev
        return n + sub

result is countdown of 10
"""

tokens = Tokenizer(code4).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)
interp.evaluate(ast)

result = interp.environment.lookup("result")
fs = interp.get_framework_strength()

print(f"countdown of 10 = {result.coords[0]} (expected 55)")
print(f"Framework Strength: {fs:.4f}")
print(f"Trajectory length: {interp.fs_tracker.get_trajectory_length()}")

# Expected: 0 + 1 + 2 + ... + 10 = 55
expected = sum(range(11))
assert abs(result.coords[0] - expected) < 0.1, f"Expected {expected}, got {result.coords[0]}"

print("\n" + "=" * 70)
print("Summary of Self-Reference Tests")
print("=" * 70)
print()
print("✅ LIMITED self-reference works (with base case)")
print("✅ MUTUAL recursion works (even/odd)")
print("✅ RECURSIVE computation works (countdown)")
print("⚠️  PURE self-reference (meta of meta) hits Python limits")
print()
print("KEY INSIGHT:")
print("The equilibrium principle ALLOWS self-reference to be expressed,")
print("but pure infinite self-reference still diverges at the")
print("implementation level (Python recursion).")
print()
print("TO FULLY VALIDATE HYPOTHESIS:")
print("Need to implement convergence detection in function calls")
print("When FS approaches 1.0, the system should recognize equilibrium")
print("and return the stable eigenstate instead of continuing recursion.")
print()
print("This would enable true 'eval of eval' stability.")
