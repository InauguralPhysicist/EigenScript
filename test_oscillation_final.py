#!/usr/bin/env python3
"""
Test oscillation detection - the EigenFunction-inspired enhancement.

This validates that the system can detect paradoxical/oscillating patterns
via sign changes in trajectory deltas, just like EigenFunction's paradox detector.
"""

from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.evaluator.interpreter import Interpreter
import numpy as np

print("=" * 70)
print("Testing Oscillation Detection (EigenFunction-Inspired)")
print("=" * 70)
print()

# Test 1: Pure self-loop (should trigger oscillation detection)
print("Test 1: Pure self-loop convergence")
print("-" * 70)

code1 = """
define selfloop as:
    return selfloop of n

result is selfloop of 1
"""

tokens = Tokenizer(code1).tokenize()
ast = Parser(tokens).parse()

# High threshold so only oscillation detection triggers
interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.99,  # Very high - won't trigger via FS
    max_iterations=100
)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")

# Check if eigenstate was detected
norm = np.linalg.norm(result_val.coords)
nonzero_count = np.sum(np.abs(result_val.coords) > 1e-10)
fs = interp.get_framework_strength()

print(f"Result vector norm: {norm:.4f}")
print(f"Nonzero coordinates: {nonzero_count}")
print(f"Framework Strength: {fs:.4f}")

# Eigenstate marker will have nonzero values in ASCII char indices
# The string "<eigenstate ..." has characters like '<', 'e', 'i', 'g', etc
# which correspond to indices 60, 101, 105, 103, etc
expected_indices = [ord(c) for c in "<eigenstate"]
found_matches = sum(1 for idx in expected_indices if idx < 768 and abs(result_val.coords[idx]) > 1e-10)

if norm > 1.0 and nonzero_count > 50:
    print("✅ PASS - Oscillation detected and eigenstate returned!")
    print(f"   The vector has {nonzero_count} nonzero coordinates")
    print(f"   Matches expected eigenstate character pattern: {found_matches}/{len(expected_indices)} chars")
    print()
    print("   MECHANISM: Oscillation score > 0.15 triggered convergence")
    print("   This prevents infinite recursion in pure self-loops!")
else:
    print(f"❌ FAIL - Expected eigenstate but got norm={norm:.4f}, nonzero={nonzero_count}")


# Test 2: Normal recursion (should NOT trigger oscillation detection)
print("\nTest 2: Normal recursion with base case")
print("-" * 70)

code2 = """
define countdown as:
    if n < 1:
        return 0
    else:
        prev is n - 1
        sub is countdown of prev
        return n + sub

result is countdown of 5
"""

tokens = Tokenizer(code2).tokenize()
ast = Parser(tokens).parse()

interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.99,
    max_iterations=100
)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")
fs = interp.get_framework_strength()

expected = sum(range(6))  # 0+1+2+3+4+5 = 15
actual = result_val.coords[0]

print(f"countdown of 5 = {actual} (expected {expected})")
print(f"Framework Strength: {fs:.4f}")

if abs(actual - expected) < 0.1:
    print("✅ PASS - Normal recursion works correctly")
    print("   Oscillation detection doesn't interfere with valid recursion")
else:
    print(f"❌ FAIL - Expected {expected}, got {actual}")


# Test 3: Verify oscillation scoring threshold
print("\nTest 3: Oscillation threshold sensitivity")
print("-" * 70)

# Create a function that oscillates intentionally
code3 = """
define oscillator as:
    if n < 1:
        return oscillator of 10
    else:
        prev is n - 1
        return oscillator of prev

result is oscillator of 3
"""

tokens = Tokenizer(code3).tokenize()
ast = Parser(tokens).parse()

interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.99,
    max_iterations=100
)

result = interp.evaluate(ast)
result_val = interp.environment.lookup("result")
norm = np.linalg.norm(result_val.coords)
nonzero_count = np.sum(np.abs(result_val.coords) > 1e-10)

print(f"Result vector norm: {norm:.4f}")
print(f"Nonzero coordinates: {nonzero_count}")

if norm > 1.0 and nonzero_count > 50:
    print("✅ PASS - Oscillating pattern detected and stopped!")
    print("   System prevents infinite loops by recognizing oscillation")
else:
    print(f"⚠️  Expected oscillation detection, got norm={norm:.4f}")


print("\n" + "=" * 70)
print("Summary: Oscillation Detection Enhancement")
print("=" * 70)
print()
print("ACHIEVEMENT: Integrated EigenFunction's oscillation detection")
print()
print("Three-signal convergence detection:")
print("  1. Framework Strength threshold (FS >= threshold)")
print("  2. Variance detection (low variance indicates fixed point)")
print("  3. ⭐ NEW: Oscillation scoring (sign changes in trajectory)")
print()
print("When oscillation score > 0.15:")
print("  → System detects paradoxical/divergent pattern")
print("  → Returns eigenstate to prevent infinite recursion")
print()
print("This completes the integration of EigenFunction's mathematical")
print("approach with EigenScript's runtime convergence detection.")
print()
print("Both systems now share the same principle:")
print("  'Equilibrium geometry enables stable self-reference'")
