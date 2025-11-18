"""
Built-in functions for EigenScript.

This module provides essential built-in functions that are pre-bound
in the global environment.
"""

from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.semantic.metric import MetricTensor
from typing import Any, Callable
import sys


class BuiltinFunction:
    """
    Wrapper for built-in functions in EigenScript.

    Built-ins are special functions implemented in Python that
    are available in the EigenScript runtime.
    """

    def __init__(self, name: str, func: Callable, space: LRVMSpace):
        """
        Initialize a built-in function.

        Args:
            name: Function name
            func: Python callable implementing the function
            space: LRVM space for vector operations
        """
        self.name = name
        self.func = func
        self.space = space

    def call(self, arg: LRVMVector) -> LRVMVector:
        """
        Call the built-in function with an LRVM vector argument.

        Args:
            arg: Argument vector

        Returns:
            Result vector
        """
        return self.func(arg, self.space)

    def __repr__(self) -> str:
        return f"<builtin {self.name}>"


def builtin_print(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Print a value to stdout.

    Syntax: print of x

    Args:
        arg: Value to print
        space: LRVM space

    Returns:
        The input value (pass-through)
    """
    # Extract scalar or string representation
    value = arg.coords[0]

    # Check if it's a string embedding (heuristic: check for ASCII-like patterns)
    # For now, just print the first coordinate
    if abs(value) < 1000 and value == int(value):
        print(int(value))
    else:
        print(value)

    return arg


def builtin_type(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Get the type of a value.

    Syntax: type of x

    Args:
        arg: Value to inspect
        space: LRVM space

    Returns:
        String vector representing the type
    """
    # Analyze the vector to determine type
    # This is a simplified heuristic

    value = arg.coords[0]

    # Check norm to determine type
    norm_sq = arg.coords @ arg.coords

    if abs(norm_sq) < 1e-10:
        return space.embed_string("null")
    elif abs(value) < 1e10 and len(set(arg.coords[1:10])) < 3:
        # Scalar-like pattern
        return space.embed_string("number")
    else:
        # Complex pattern (string, list, or function)
        return space.embed_string("complex")


def builtin_norm(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Compute the norm of a vector.

    Syntax: norm of x

    Args:
        arg: Vector to measure
        space: LRVM space

    Returns:
        Scalar vector with norm value
    """
    # Compute Euclidean norm
    norm_sq = float(arg.coords @ arg.coords)
    norm = norm_sq ** 0.5
    return space.embed_scalar(norm)


def builtin_len(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Get the length/magnitude of a value.

    Syntax: len of x

    Args:
        arg: Value to measure
        space: LRVM space

    Returns:
        Scalar vector with length
    """
    # For now, return the number of non-zero coordinates
    # This gives a sense of "complexity" or "size"
    nonzero = (abs(arg.coords) > 1e-10).sum()
    return space.embed_scalar(float(nonzero))


def builtin_first(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Get the first element of a list/vector.

    Syntax: first of list

    Args:
        arg: List vector
        space: LRVM space

    Returns:
        First element as scalar
    """
    # Return first coordinate as embedded scalar
    return space.embed_scalar(arg.coords[0])


def builtin_rest(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Get all but the first element of a list/vector.

    Syntax: rest of list

    Args:
        arg: List vector
        space: LRVM space

    Returns:
        Remaining elements as vector
    """
    # Shift coordinates left, zero-padding at end
    coords = arg.coords.copy()
    coords[:-1] = coords[1:]
    coords[-1] = 0.0
    return LRVMVector(coords)


def builtin_empty(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Check if a list/vector is empty.

    Syntax: empty of list

    Args:
        arg: List vector to check
        space: LRVM space

    Returns:
        1.0 if empty, 0.0 otherwise
    """
    # Empty if norm is approximately zero
    norm_sq = float(arg.coords @ arg.coords)
    is_empty = 1.0 if norm_sq < 1e-10 else 0.0
    return space.embed_scalar(is_empty)


def builtin_fs(arg: LRVMVector, space: LRVMSpace) -> LRVMVector:
    """
    Get current Framework Strength.

    Syntax: fs of null

    Note: This needs access to the interpreter's FS tracker.
    For now, returns a placeholder. Will be properly implemented
    by the interpreter.

    Args:
        arg: Ignored (use null)
        space: LRVM space

    Returns:
        Current FS value
    """
    # Placeholder - interpreter will override this
    return space.embed_scalar(0.0)


# Registry of built-in functions
BUILTIN_NAMES = [
    "print",
    "type",
    "norm",
    "len",
    "first",
    "rest",
    "empty",
    "fs"
]


def create_builtins(space: LRVMSpace) -> dict[str, BuiltinFunction]:
    """
    Create all built-in functions for a given LRVM space.

    Args:
        space: LRVM space for vector operations

    Returns:
        Dictionary mapping names to BuiltinFunction objects
    """
    return {
        "print": BuiltinFunction("print", builtin_print, space),
        "type": BuiltinFunction("type", builtin_type, space),
        "norm": BuiltinFunction("norm", builtin_norm, space),
        "len": BuiltinFunction("len", builtin_len, space),
        "first": BuiltinFunction("first", builtin_first, space),
        "rest": BuiltinFunction("rest", builtin_rest, space),
        "empty": BuiltinFunction("empty", builtin_empty, space),
        "fs": BuiltinFunction("fs", builtin_fs, space),
    }
