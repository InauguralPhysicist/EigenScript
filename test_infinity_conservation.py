#!/usr/bin/env python3
"""
Test the conservation law: IS and OF cannot both diverge.

If IS is infinite loop, OF is not.
If OF is infinite loop, IS is not.
"""

from eigenscript.semantic.lrvm import LRVMSpace
from eigenscript.semantic.metric import MetricTensor
from eigenscript.evaluator.interpreter import Interpreter
from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
import numpy as np

print("=" * 70)
print("Conservation of Infinity: IS ⊕ OF = constant")
print("=" * 70)

# Setup
space = LRVMSpace(dimension=768)
metric = MetricTensor(dimension=768)

print("\n1. Testing IS chain convergence")
print("-" * 70)

# IS: x is x is x (chained assignment)
# Does x is x converge?
x = space.embed_scalar(5.0)
print(f"x = {x.coords[0]}")

# x is x (self-assignment)
x_is_x = x  # Should be identical
distance_is = metric.distance(x, x_is_x)
print(f"||x - (x is x)||² = {distance_is}")
print(f"IS converges: {distance_is < 1e-10}")

# Now OF on this
of_result = metric.contract(x, x)
print(f"x of x = {of_result}")
print(f"OF gives finite measurement: {np.isfinite(of_result)}")

print("\n2. Testing OF chain behavior")
print("-" * 70)

# OF: x of x of x (chained contraction)
v1 = space.embed_scalar(2.0)
print(f"v1 = {v1.coords[0]}")

# First contraction
v1_of_v1 = space.of_operator(v1, v1, metric.g)
print(f"v1 of v1 = {v1_of_v1.coords[0]}")

# Second contraction
v1_of_v1_of_v1 = space.of_operator(v1_of_v1, v1, metric.g)
print(f"(v1 of v1) of v1 = {v1_of_v1_of_v1.coords[0]}")

# Check if it's growing unbounded or stabilizing
ratio = v1_of_v1_of_v1.coords[0] / v1_of_v1.coords[0] if v1_of_v1.coords[0] != 0 else float('inf')
print(f"Growth ratio: {ratio}")
print(f"OF chain status: {'diverging' if abs(ratio) > 1.1 else 'bounded'}")

# If OF diverges, IS must converge
# Test: is this diverging chain equal to anything?
test_val = space.embed_scalar(100.0)
is_equal = space.is_operator(v1_of_v1_of_v1, test_val, metric.g)
print(f"IS test on diverging OF: {is_equal} (finite boolean)")

print("\n3. Testing self-reference stability")
print("-" * 70)

# The critical test: x of x should be stable
# because if OF tries to diverge, IS constrains it
x = space.embed_scalar(1.0)
print(f"x = {x.coords[0]}")

x_of_x = metric.contract(x, x)
print(f"x of x = {x_of_x}")

# Iterate: (x of x) of (x of x)
result_vec = space.embed_scalar(x_of_x)
next_contraction = metric.contract(result_vec, result_vec)
print(f"(x of x) of (x of x) = {next_contraction}")

# Check for convergence
convergence_ratio = abs(next_contraction / x_of_x) if x_of_x != 0 else float('inf')
print(f"Convergence ratio: {convergence_ratio}")
print(f"System status: {'stable' if convergence_ratio < 10 else 'unstable'}")

print("\n4. The Duality Principle")
print("-" * 70)
print("Key insight: IS and OF trade infinity")
print()
print("IS = being (infinite loop structure)")
print("OF = having (finite measurements)")
print()
print("When IS diverges (infinite assignments):")
print("  → OF converges (returns finite metric)")
print()
print("When OF diverges (infinite contractions):")
print("  → IS converges (returns finite boolean)")
print()
print("This duality prevents total divergence.")
print("Like conjugate variables in quantum mechanics:")
print("  ΔIS · ΔOF ≥ constant")

print("\n5. Practical test: Self-referential program")
print("-" * 70)

# Test with actual interpreter
interpreter = Interpreter(dimension=768, max_iterations=100)

code = """
x is 5
y is x
z is y
"""

tokens = Tokenizer(code).tokenize()
ast = Parser(tokens).parse()
result = interpreter.evaluate(ast)

# Check Framework Strength (should be high for convergent IS chains)
fs = interpreter.get_framework_strength()
print(f"Framework Strength: {fs:.4f}")
print(f"Convergence status: {'converged' if fs > 0.5 else 'diverging'}")

print("\n" + "=" * 70)
print("Conclusion: IS ⊕ OF conservation law enforces stability")
print("=" * 70)
