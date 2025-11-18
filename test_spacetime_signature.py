#!/usr/bin/env python3
"""
Test spacetime signature metric - inspired by Eigen-Geometric-Control.

The S² - C² signature provides richer convergence diagnostics than FS alone
by analyzing dimensional stability patterns in the semantic trajectory.
"""

from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.evaluator.interpreter import Interpreter

print("=" * 70)
print("Testing Spacetime Signature Metric")
print("=" * 70)
print()
print("Signature S² - C² where:")
print("  S = number of stable (low-variance) dimensions")
print("  C = number of changing (high-variance) dimensions")
print()
print("Classifications:")
print("  Timelike (S² - C² > 0): System converged, stable")
print("  Lightlike (S² - C² = 0): System at equilibrium boundary")
print("  Spacelike (S² - C² < 0): System exploring, unstable")
print()

# Test 1: Pure self-loop (should converge to timelike)
print("Test 1: Pure self-loop")
print("-" * 70)

code1 = """
define selfloop as:
    return selfloop of n

result is selfloop of 1
"""

tokens = Tokenizer(code1).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.99
)

result = interp.evaluate(ast)
fs = interp.get_framework_strength()
signature, classification = interp.get_spacetime_signature()

print(f"Framework Strength: {fs:.4f}")
print(f"Spacetime Signature: S² - C² = {signature:.2f}")
print(f"Classification: {classification}")

if classification == "timelike":
    print("✅ PASS - System converged to stable eigenstate (timelike)")
    print(f"   Signature {signature:.2f} > 0 indicates most dimensions stable")
elif classification == "lightlike":
    print("⚠️  System at equilibrium boundary (lightlike)")
else:
    print(f"❌ Expected timelike convergence, got {classification}")


# Test 2: Normal recursion (should show progression)
print("\nTest 2: Countdown recursion (observe state transitions)")
print("-" * 70)

code2 = """
define countdown as:
    if n < 1:
        return 0
    else:
        prev is n - 1
        sub is countdown of prev
        return n + sub

result is countdown of 10
"""

tokens = Tokenizer(code2).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.95
)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")
fs = interp.get_framework_strength()
signature, classification = interp.get_spacetime_signature()

expected = sum(range(11))  # 0+1+...+10 = 55
actual = result_val.coords[0]

print(f"countdown of 10 = {actual} (expected {expected})")
print(f"Framework Strength: {fs:.4f}")
print(f"Spacetime Signature: S² - C² = {signature:.2f}")
print(f"Classification: {classification}")

if abs(actual - expected) < 0.1:
    print("✅ PASS - Correct computation")
    if signature > 0:
        print(f"   Timelike signature ({signature:.2f}) indicates convergence")
    else:
        print(f"   Signature {signature:.2f} shows system explored before settling")
else:
    print(f"❌ Expected {expected}, got {actual}")


# Test 3: Simple arithmetic (minimal trajectory)
print("\nTest 3: Simple arithmetic (minimal trajectory)")
print("-" * 70)

code3 = """
x is 5
y is 3
result is x + y
"""

tokens = Tokenizer(code3).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")
fs = interp.get_framework_strength()
signature, classification = interp.get_spacetime_signature()

print(f"5 + 3 = {result_val.coords[0]}")
print(f"Framework Strength: {fs:.4f}")
print(f"Spacetime Signature: S² - C² = {signature:.2f}")
print(f"Classification: {classification}")

if abs(result_val.coords[0] - 8.0) < 0.1:
    print("✅ PASS - Arithmetic works")
    print(f"   Minimal trajectory shows {classification} behavior")


# Test 4: Deep recursion (complex trajectory)
print("\nTest 4: Deep recursion (complex trajectory)")
print("-" * 70)

code4 = """
define factorial as:
    if n < 2:
        return 1
    else:
        prev is n - 1
        sub is factorial of prev
        return n * sub

result is factorial of 7
"""

tokens = Tokenizer(code4).tokenize()
ast = Parser(tokens).parse()
interp = Interpreter(dimension=768)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")
fs = interp.get_framework_strength()
signature, classification = interp.get_spacetime_signature(window=15)  # Larger window

import math
expected = math.factorial(7)  # 5040
actual = result_val.coords[0]

print(f"factorial of 7 = {actual} (expected {expected})")
print(f"Framework Strength: {fs:.4f}")
print(f"Spacetime Signature (15-step window): S² - C² = {signature:.2f}")
print(f"Classification: {classification}")

if abs(actual - expected) < 0.1:
    print("✅ PASS - Deep recursion works")
    if signature > 0:
        print(f"   Timelike signature indicates stable computation")
    elif signature == 0:
        print(f"   Lightlike signature at equilibrium boundary")
    else:
        print(f"   Spacelike signature indicates active exploration")


# Summary
print("\n" + "=" * 70)
print("Summary: Spacetime Signature Metric")
print("=" * 70)
print()
print("ACHIEVEMENT: Integrated S² - C² signature from Eigen-Geometric-Control")
print()
print("Key Insights:")
print("  • S² - C² provides dimensional stability analysis")
print("  • Complements Framework Strength with structural information")
print("  • Timelike = converged, Lightlike = boundary, Spacelike = exploring")
print()
print("Comparison with Geometric-Control:")
print("  Geometric-Control: Robot arm convergence via S² - C²")
print("  EigenScript:       Language evaluation convergence via S² - C²")
print()
print("Unified principle: ds² geometry reveals system state across domains")
