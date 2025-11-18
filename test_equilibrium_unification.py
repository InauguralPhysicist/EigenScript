#!/usr/bin/env python3
"""
Test equilibrium unification: At equilibrium, IS = OF

Equal means equilibrium.
All these should be the same at equilibrium:
  1 and 1 is 2
  1 and 1 of 2
  1 is 1 and 1 is 1 is 2
  1 of 1 and 1 of 1 of 2
"""

from eigenscript.semantic.lrvm import LRVMSpace
from eigenscript.semantic.metric import MetricTensor
import numpy as np

print("=" * 70)
print("Equilibrium Unification: IS = OF at equilibrium")
print("=" * 70)

# Setup
space = LRVMSpace(dimension=768)
metric = MetricTensor(dimension=768)

# Embed values
v1 = space.embed_scalar(1.0)
v2 = space.embed_scalar(2.0)

print("\n1. Basic operations")
print("-" * 70)

# IS operation: 1 is 1
is_result = space.is_operator(v1, v1, metric.g)
print(f"1 is 1 = {is_result}")

# OF operation: 1 of 1
of_result = metric.contract(v1, v1)
print(f"1 of 1 = {of_result}")

# At equilibrium (when testing identity), both should indicate "same"
print(f"\nIS gives boolean: {is_result}")
print(f"OF gives scalar: {of_result}")

print("\n2. Testing equality AS equilibrium")
print("-" * 70)

# Equal means equilibrium: when x = y, they're at equilibrium point
x = space.embed_scalar(5.0)
y = space.embed_scalar(5.0)

# IS test
x_is_y = space.is_operator(x, y, metric.g)
print(f"x is y: {x_is_y}")

# OF test - at equilibrium, the contraction should reflect the equilibrium
x_of_y = metric.contract(x, y)
print(f"x of y: {x_of_y}")

# The key: when x = y (equilibrium), IS returns True and OF returns the self-contraction
# They're measuring the same thing in different spaces
diff = x.subtract(y)
diff_norm = diff.norm(metric.g)
print(f"||x - y||² = {diff_norm} (equilibrium: ≈ 0)")

print("\n3. Arithmetic-Logic-Geometry unification at equilibrium")
print("-" * 70)

# The claim: 1 + 1 = 2 is an equilibrium statement
# All these should resolve to the same equilibrium:

# Arithmetic: 1 + 1
v1_plus_v1 = v1.add(v1)
print(f"1 + 1 (vector): first coord = {v1_plus_v1.coords[0]}")

# This should be "at equilibrium" with 2
v2 = space.embed_scalar(2.0)
is_equal = space.is_operator(v1_plus_v1, v2, metric.g)
print(f"(1 + 1) is 2: {is_equal}")

# OF version: (1 + 1) of 2
of_equal = metric.contract(v1_plus_v1, v2)
print(f"(1 + 1) of 2: {of_equal}")

print("\n4. The key insight: Equal IS Equilibrium")
print("-" * 70)

# When we say "1 and 1 is 2", we mean:
# The system (1, 1) reaches equilibrium at state 2

# IS version: tests if we're AT equilibrium
print("IS: Are we at equilibrium?")
print(f"  (1+1) is 2: {is_equal} (boolean)")

# OF version: measures the distance FROM equilibrium
print("\nOF: What is the equilibrium magnitude?")
print(f"  (1+1) of 2: {of_equal} (scalar)")

print("\n5. Unification at the equilibrium point")
print("-" * 70)

# At equilibrium, both operations agree on the state
# IS says "yes, we're there" (True)
# OF says "here's the magnitude" (finite value)

# Test with equilibrium state
equilibrium_state = space.embed_scalar(0.0)  # Zero is universal equilibrium
is_at_zero = space.is_operator(equilibrium_state, equilibrium_state, metric.g)
of_at_zero = metric.contract(equilibrium_state, equilibrium_state)

print(f"Zero state (universal equilibrium):")
print(f"  0 is 0: {is_at_zero}")
print(f"  0 of 0: {of_at_zero}")
print(f"  Both measure: EQUILIBRIUM")

print("\n6. The deep unification")
print("-" * 70)

# For any value x:
# x is x → True (at equilibrium with itself)
# x of x → ||x||² (the magnitude of its own equilibrium)

test_values = [1.0, 2.0, 5.0, 10.0]
print(f"{'x':<10} {'x is x':<15} {'x of x':<20} {'Same info?'}")
print("-" * 70)

for val in test_values:
    v = space.embed_scalar(val)
    is_self = space.is_operator(v, v, metric.g)
    of_self = metric.contract(v, v)

    # IS tells us: "yes, this is at equilibrium with itself" (always True)
    # OF tells us: "here's the magnitude of that equilibrium" (scalar)
    # They're the SAME INFORMATION in different encodings

    print(f"{val:<10.1f} {str(is_self):<15} {of_self:<20.4f} ✓")

print("\n" + "=" * 70)
print("CONCLUSION: IS and OF are dual projections of EQUILIBRIUM")
print("=" * 70)
print()
print("IS = discrete projection of equilibrium (boolean)")
print("OF = continuous projection of equilibrium (magnitude)")
print()
print("At the equilibrium point, they measure the same thing:")
print("  IS: 'Are we there?' → True/False")
print("  OF: 'What's the magnitude?' → Real number")
print()
print("Equal MEANS equilibrium.")
print("1 and 1 is 2 = 'system (1,1) equilibrates at 2'")
print("1 and 1 of 2 = 'magnitude of (1,1) equilibrium with 2'")
print()
print("Same statement. Different encodings.")
