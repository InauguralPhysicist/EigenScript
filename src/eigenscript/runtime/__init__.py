"""
Runtime module for EigenScript.

This module handles runtime state management including:
- Framework Strength measurement
- Convergence detection
- Built-in functions
"""

from eigenscript.runtime.eigencontrol import EigenControlTracker

__all__ = ["EigenControlTracker"]
