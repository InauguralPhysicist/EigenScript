#!/usr/bin/env python3
"""
Test function execution - the critical feature for self-hosting.
"""

from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.evaluator.interpreter import Interpreter

print("=" * 70)
print("Testing Function Execution")
print("=" * 70)

# Test 1: Simple function that returns a constant
print("\n1. Simple constant function")
print("-" * 70)

code1 = """
define get_five as:
    return 5

result is get_five of 0
"""

tokens = Tokenizer(code1).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)
interp.evaluate(ast)

result = interp.environment.lookup("result")
print(f"get_five of 0 = {result.coords[0]}")
assert result.coords[0] == 5.0, f"Expected 5.0, got {result.coords[0]}"
print("✅ PASS")

# Test 2: Function that uses parameter 'n'
print("\n2. Function using parameter 'n'")
print("-" * 70)

code2 = """
define double as:
    result is n * 2
    return result

x is double of 7
"""

tokens = Tokenizer(code2).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)
interp.evaluate(ast)

x = interp.environment.lookup("x")
print(f"double of 7 = {x.coords[0]}")
assert x.coords[0] == 14.0, f"Expected 14.0, got {x.coords[0]}"
print("✅ PASS")

# Test 3: Recursive factorial (iterative version first)
print("\n3. Iterative factorial")
print("-" * 70)

code3 = """
n is 5
result is 1
counter is 1

loop while counter < (n + 1):
    result is result * counter
    counter is counter + 1
"""

tokens = Tokenizer(code3).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768, max_iterations=100)
interp.evaluate(ast)

result = interp.environment.lookup("result")
print(f"5! (iterative) = {result.coords[0]}")
assert result.coords[0] == 120.0, f"Expected 120.0, got {result.coords[0]}"
print("✅ PASS")

# Test 4: Recursive factorial
print("\n4. Recursive factorial")
print("-" * 70)

code4 = """
define factorial as:
    if n < 2:
        return 1
    else:
        prev is n - 1
        sub_result is factorial of prev
        return n * sub_result

result is factorial of 5
"""

tokens = Tokenizer(code4).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)
interp.evaluate(ast)

result = interp.environment.lookup("result")
print(f"factorial of 5 = {result.coords[0]}")
assert result.coords[0] == 120.0, f"Expected 120.0, got {result.coords[0]}"
print("✅ PASS - RECURSIVE FUNCTIONS WORK!")

# Test 5: Check Framework Strength during recursion
print("\n5. Framework Strength during recursive computation")
print("-" * 70)

fs = interp.get_framework_strength()
print(f"Framework Strength: {fs:.4f}")
print(f"Convergence status: {'CONVERGED' if fs > 0.5 else 'diverging'}")

print("\n" + "=" * 70)
print("ALL FUNCTION TESTS PASSED!")
print("=" * 70)
print()
print("Key achievements:")
print("✅ Functions can be defined and called")
print("✅ Parameters are properly bound")
print("✅ Return statements work")
print("✅ RECURSIVE CALLS WORK")
print()
print("Next step: Test self-reference stability (eval of eval)")
