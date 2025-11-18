#!/usr/bin/env python3
"""
Test the duality between IS and OF operators.

Exploring: "IS is a projection of OF, OF is a projection of IS"
"""

from eigenscript.semantic.lrvm import LRVMSpace
from eigenscript.semantic.metric import MetricTensor
import numpy as np

# Setup
space = LRVMSpace(dimension=768)
metric = MetricTensor(dimension=768, metric_type="euclidean")

# Embed the value 1
v1_a = space.embed_scalar(1.0)
v1_b = space.embed_scalar(1.0)

print("=" * 60)
print("Testing: 1 is 1")
print("=" * 60)

# IS operator: x is y ⟺ ||x - y||² ≈ 0
is_result = space.is_operator(v1_a, v1_b, metric.g)
print(f"1 is 1 = {is_result}")

# What's the actual distance?
diff = v1_a.subtract(v1_b)
norm_sq = diff.norm(metric.g)
print(f"||1 - 1||² = {norm_sq}")

print()
print("=" * 60)
print("Testing: 1 of 1")
print("=" * 60)

# OF operator: x of y → x^T g y
of_result = space.of_operator(v1_a, v1_b, metric.g)
print(f"1 of 1 = {of_result.coords[0]}")  # First coordinate holds the scalar

# What's the actual contraction?
contraction = metric.contract(v1_a, v1_b)
print(f"1^T g 1 = {contraction}")

print()
print("=" * 60)
print("The Duality")
print("=" * 60)

# IS tests if OF of difference is zero
diff_of_diff = metric.contract(diff, diff)
print(f"(1-1) of (1-1) = {diff_of_diff}")
print(f"This is zero? {abs(diff_of_diff) < 1e-10}")
print(f"Same as IS result? {(abs(diff_of_diff) < 1e-10) == is_result}")

print()

# OF computes the magnitude that IS tests
print(f"OF gives the value: {contraction}")
print(f"IS tests if that value (for difference) ≈ 0: {is_result}")

print()
print("=" * 60)
print("Structural Symmetry")
print("=" * 60)

print("IS: binary operator → boolean")
print("OF: binary operator → scalar")
print()
print("IS = π_bool(OF)  (project OF onto {0,1})")
print("OF = π_ℝ(IS)     (project IS onto ℝ)")
