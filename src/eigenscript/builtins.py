"""
Built-in functions for EigenScript.

Provides standard library functions like print, input, len, etc.
"""

import sys
import math
import numpy as np
from typing import Callable, Any, Union
from dataclasses import dataclass
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace

# Type alias for values that can flow through the interpreter
# Must match the Value type in interpreter.py
Value = Union[LRVMVector, "EigenList"]


@dataclass
class BuiltinFunction:
    """
    Represents a built-in function implemented in Python.
    
    Built-in functions are native code that can be called from EigenScript.
    They receive Values (LRVM vectors or lists) and context (space + metric) 
    and return Values.
    """
    name: str
    func: Callable[[Value, 'LRVMSpace', Any], Value]  # Takes (arg, space, metric)
    description: str = ""
    
    def __repr__(self) -> str:
        return f"BuiltinFunction({self.name!r})"


def builtin_print(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Print a value to stdout.
    
    Args:
        arg: LRVM vector or EigenList to print
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Null vector (prints have no meaningful return value)
    """
    # Import here to avoid circular dependency
    from eigenscript.evaluator.interpreter import EigenList
    
    # Handle EigenList
    if isinstance(arg, EigenList):
        # Print list as [elem1, elem2, ...] (handles empty lists)
        if len(arg.elements) == 0:
            print("[]")
        else:
            decoded_elems = []
            for elem in arg.elements:
                decoded_elems.append(decode_vector(elem, space, metric))
            print(f"[{', '.join(str(e) for e in decoded_elems)}]")
    else:
        # Regular vector
        value = decode_vector(arg, space, metric)
        print(value)
    
    return space.zero_vector()


def builtin_input(prompt: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Read a line from stdin.
    
    Args:
        prompt: Prompt message as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        User input as LRVM vector
    """
    prompt_str = decode_vector(prompt, space, metric)
    user_input = input(str(prompt_str))
    return space.embed(user_input)


def builtin_len(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Get the length of a value.
    
    For lists: returns the number of elements.
    For vectors: returns the Euclidean norm.
    
    Args:
        arg: LRVM vector or EigenList
        space: LRVM space for operations
        metric: Metric tensor for computing norm
        
    Returns:
        Length as LRVM vector
    """
    # Import here to avoid circular dependency
    from eigenscript.evaluator.interpreter import EigenList
    
    # Handle EigenList
    if isinstance(arg, EigenList):
        return space.embed(float(len(arg.elements)))
    else:
        # For vectors, return the Euclidean norm
        norm_value = np.linalg.norm(arg.coords)
        return space.embed(float(norm_value))


def builtin_type(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Get the type of a value.
    
    Args:
        arg: LRVM vector or EigenList
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Type name as LRVM vector
    """
    # Import here to avoid circular dependency
    from eigenscript.evaluator.interpreter import EigenList
    
    # Handle EigenList
    if isinstance(arg, EigenList):
        return space.embed("list")
    else:
        value = decode_vector(arg, space, metric)
        type_name = type(value).__name__
        return space.embed(type_name)


def builtin_norm(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Get the geometric norm (magnitude) of a vector.
    
    Args:
        arg: LRVM vector
        space: LRVM space for operations
        metric: Metric tensor for computing norm
        
    Returns:
        Norm as LRVM vector
    """
    # Use Euclidean norm for simplicity
    norm_value = np.linalg.norm(arg.coords)
    return space.embed(float(norm_value))


def builtin_range(arg: LRVMVector, space: LRVMSpace, metric: Any = None):
    """
    Generate a range of numbers from 0 to n-1.
    
    Creates a list containing integers [0, 1, 2, ..., n-1].
    
    Example:
        range of 5  # Creates [0, 1, 2, 3, 4]
    
    Args:
        arg: Upper limit as LRVM vector (will be converted to integer)
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        EigenList containing numbers [0, 1, ..., n-1]
    """
    # Import here to avoid circular dependency
    from eigenscript.evaluator.interpreter import EigenList
    
    # Properly decode the vector to get the actual number
    decoded_value = decode_vector(arg, space, metric)
    
    # Handle both int and float results
    if isinstance(decoded_value, (int, float)):
        n = int(decoded_value)
    else:
        # Fallback: try to parse as string or use default
        try:
            n = int(decoded_value)
        except (ValueError, TypeError):
            n = 0
    
    # Generate list elements as LRVM vectors
    elements = []
    for i in range(n):
        elements.append(space.embed_scalar(float(i)))
    
    return EigenList(elements)


def decode_vector(vector: Value, space: LRVMSpace, metric: Any = None) -> Any:
    """
    Attempt to decode a Value (LRVM vector or list) back to a Python value.
    
    This is a best-effort heuristic decoder. Since LRVM embeddings
    are lossy, we can't always perfectly reconstruct the original value.
    
    Args:
        vector: LRVM vector or EigenList to decode
        space: LRVM space for context
        metric: Metric tensor (optional)
        
    Returns:
        Decoded Python value (str, float, list, or vector representation)
    """
    # Import here to avoid circular dependency
    from eigenscript.evaluator.interpreter import EigenList
    
    # Handle EigenList - return the list itself
    if isinstance(vector, EigenList):
        # Decode each element in the list recursively
        return [decode_vector(elem, space, metric) for elem in vector.elements]
    
    # Check for string metadata first (strings preserve their original value)
    if "string_value" in vector.metadata:
        return vector.metadata["string_value"]
    
    # Check if it's approximately the zero vector
    if np.allclose(vector.coords, 0.0, atol=1e-6):
        return "null"
    
    # For scalar embeddings, the first coordinate contains the actual value
    # Check coords[0] and coords[1] - if they're both close to the same value,
    # it's likely a scalar embedding
    first_coord = vector.coords[0]
    second_coord = vector.coords[1] if len(vector.coords) > 1 else 0.0
    
    # Scalar embeddings have coords[0] and coords[1] set to the value
    # Handle zero specially
    if abs(first_coord) < 1e-9 and abs(second_coord) < 1e-9:
        # Check if this looks like zero (coords[2] should also be small for zero)
        third_coord = vector.coords[2] if len(vector.coords) > 2 else 0.0
        if abs(third_coord) < 1.5:  # Zero has coords[2] ≈ 1
            return 0
    
    # Check for scalar embedding: coords[0] = value, coords[1] = value (or abs(value) in some cases)
    # Handle both cases: coords[1] = value (same as coords[0]) or coords[1] = abs(value)
    if abs(first_coord) > 1e-9:
        # Case 1: coords[0] and coords[1] are the same (including negative numbers)
        if abs(first_coord - second_coord) < 1e-6:
            # Likely a scalar - return as int if close to integer
            if abs(first_coord - round(first_coord)) < 1e-6:
                return int(round(first_coord))
            else:
                return first_coord
        # Case 2: coords[0] = value, coords[1] = abs(value)
        elif abs(abs(first_coord) - second_coord) < 1e-6:
            # Likely a scalar (positive or negative) - return as int if close to integer
            if abs(first_coord - round(first_coord)) < 1e-6:
                return int(round(first_coord))
            else:
                return first_coord
    
    # Check if only first coordinate is non-zero (alternative scalar encoding)
    rest_norm = np.linalg.norm(vector.coords[1:])
    if rest_norm < 1e-3 and abs(first_coord) > 1e-9:
        # Return as int or float
        if abs(first_coord - round(first_coord)) < 1e-6:
            return int(round(first_coord))
        else:
            return first_coord
    
    # Otherwise return a vector representation
    norm_value = np.linalg.norm(vector.coords)
    return f"Vector(norm={norm_value:.3f})"


def builtin_upper(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Convert string to uppercase.
    
    Example:
        upper of "hello"  -> "HELLO"
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, str):
        return space.embed_string(decoded.upper())
    else:
        raise TypeError(f"upper requires a string argument")


def builtin_lower(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Convert string to lowercase.
    
    Example:
        lower of "HELLO"  -> "hello"
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, str):
        return space.embed_string(decoded.lower())
    else:
        raise TypeError(f"lower requires a string argument")


def builtin_split(arg: LRVMVector, space: LRVMSpace, metric: Any = None):
    """
    Split string into list of words.
    
    Example:
        split of "hello world"  -> ["hello", "world"]
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, str):
        # Split by whitespace
        words = decoded.split()
        # Convert each word to an LRVM vector
        word_vectors = [space.embed_string(word) for word in words]
        return EigenList(word_vectors)
    else:
        raise TypeError(f"split requires a string argument")


def builtin_join(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Join list of strings into a single string.
    
    Example:
        join of ["hello", "world"]  -> "hello world"
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    if not isinstance(arg, EigenList):
        raise TypeError(f"join requires a list argument")
    
    # Decode each element as a string
    strings = []
    for elem in arg.elements:
        decoded = decode_vector(elem, space, metric)
        if isinstance(decoded, str):
            strings.append(decoded)
        else:
            # Convert to string representation
            strings.append(str(decoded))
    
    # Join with space separator
    result = " ".join(strings)
    return space.embed_string(result)


def builtin_append(list_and_value, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Append an element to a list (mutates the list in place).
    
    Args:
        list_and_value: Two-element list [target_list, value_to_append]
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Null vector (append has no meaningful return value)
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    # Expect list_and_value to be an EigenList with 2 elements: [list, value]
    if not isinstance(list_and_value, EigenList):
        raise TypeError("append requires a list and a value")
    
    if len(list_and_value.elements) != 2:
        raise TypeError("append requires exactly 2 arguments: list and value")
    
    target_list = list_and_value.elements[0]
    value = list_and_value.elements[1]
    
    # First element must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("First argument to append must be a list")
    
    # Append the value to the list
    target_list.append(value)
    
    return space.zero_vector()


def builtin_min(target_list, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Find the minimum value in a list.
    
    Args:
        target_list: The list to find minimum from
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        The minimum element as an LRVM vector
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    # Must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("min requires a list")
    
    if len(target_list.elements) == 0:
        raise ValueError("min of empty list is undefined")
    
    # Find minimum by decoding values and comparing
    min_elem = target_list.elements[0]
    min_value = decode_vector(min_elem, space, metric)
    
    for elem in target_list.elements[1:]:
        value = decode_vector(elem, space, metric)
        if value < min_value:
            min_value = value
            min_elem = elem
    
    return min_elem


def builtin_max(target_list, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Find the maximum value in a list.
    
    Args:
        target_list: The list to find maximum from
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        The maximum element as an LRVM vector
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    # Must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("max requires a list")
    
    if len(target_list.elements) == 0:
        raise ValueError("max of empty list is undefined")
    
    # Find maximum by decoding values and comparing
    max_elem = target_list.elements[0]
    max_value = decode_vector(max_elem, space, metric)
    
    for elem in target_list.elements[1:]:
        value = decode_vector(elem, space, metric)
        if value > max_value:
            max_value = value
            max_elem = elem
    
    return max_elem


def builtin_sort(target_list, space: LRVMSpace, metric: Any = None):
    """
    Sort a list in ascending order (returns a new sorted list).
    
    Args:
        target_list: The list to sort
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        A new sorted EigenList
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    # Must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("sort requires a list")
    
    if len(target_list.elements) == 0:
        return EigenList([])
    
    # Create list of (decoded_value, original_vector) pairs for sorting
    pairs = []
    for elem in target_list.elements:
        value = decode_vector(elem, space, metric)
        pairs.append((value, elem))
    
    # Sort by the decoded values
    sorted_pairs = sorted(pairs, key=lambda x: x[0])
    
    # Extract the sorted vectors
    sorted_elements = [pair[1] for pair in sorted_pairs]
    
    return EigenList(sorted_elements)


def builtin_pop(target_list, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Remove and return the last element from a list.
    
    Args:
        target_list: The list to pop from
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        The popped element as an LRVM vector
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    # Must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("pop requires a list")
    
    # Pop and return the element
    try:
        return target_list.pop()
    except IndexError as e:
        raise RuntimeError(str(e))


def builtin_map(args, space: LRVMSpace, metric: Any = None):
    """
    Transform each element in a list using a function.
    
    Map applies a function to every element in a list, returning a new list
    with the transformed values. This is a fundamental functional programming
    operation that leverages EigenScript's geometric semantics.
    
    Example:
        define double as:
            return arg * 2
        
        numbers is [1, 2, 3, 4, 5]
        doubled is map of [double, numbers]
        # doubled = [2, 4, 6, 8, 10]
    
    Args:
        args: Two-element list [function, target_list]
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        A new EigenList with the function applied to each element
    """
    from eigenscript.evaluator.interpreter import EigenList, Function, BuiltinFunction
    
    # Expect args to be an EigenList with 2 elements: [function, list]
    if not isinstance(args, EigenList):
        raise TypeError("map requires a function and a list")
    
    if len(args.elements) != 2:
        raise TypeError("map requires exactly 2 arguments: function and list")
    
    func = args.elements[0]
    target_list = args.elements[1]
    
    # Function must be a Function or BuiltinFunction object
    if not isinstance(func, (Function, BuiltinFunction)):
        raise TypeError("First argument to map must be a function")
    
    # Second argument must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("Second argument to map must be a list")
    
    # Apply the function to each element
    result_elements = []
    for elem in target_list.elements:
        # Call the function with the element
        if isinstance(func, Function):
            # Use the interpreter stored in the function
            if func.interpreter is None:
                raise RuntimeError("Cannot call user-defined function from map without interpreter context")
            result = func.interpreter._call_function_with_value(func, elem)
        elif isinstance(func, BuiltinFunction):
            result = func.func(elem, space, metric)
        
        result_elements.append(result)
    
    return EigenList(result_elements)


def builtin_filter(args, space: LRVMSpace, metric: Any = None):
    """
    Select elements from a list that match a criteria function.
    
    Filter applies a predicate function to each element, keeping only those
    for which the function returns a truthy value (non-zero number or non-empty string).
    
    Example:
        define is_positive as:
            return arg > 0
        
        numbers is [-2, -1, 0, 1, 2, 3]
        positives is filter of [is_positive, numbers]
        # positives = [1, 2, 3]
    
    Args:
        args: Two-element list [predicate_function, target_list]
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        A new EigenList containing only elements where predicate returns true
    """
    from eigenscript.evaluator.interpreter import EigenList, Function, BuiltinFunction
    
    # Expect args to be an EigenList with 2 elements: [function, list]
    if not isinstance(args, EigenList):
        raise TypeError("filter requires a function and a list")
    
    if len(args.elements) != 2:
        raise TypeError("filter requires exactly 2 arguments: function and list")
    
    predicate = args.elements[0]
    target_list = args.elements[1]
    
    # Predicate must be a Function or BuiltinFunction object
    if not isinstance(predicate, (Function, BuiltinFunction)):
        raise TypeError("First argument to filter must be a function")
    
    # Second argument must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("Second argument to filter must be a list")
    
    # Apply the predicate to each element and keep truthy results
    result_elements = []
    for elem in target_list.elements:
        # Call the predicate with the element
        if isinstance(predicate, Function):
            # Use the interpreter stored in the function
            if predicate.interpreter is None:
                raise RuntimeError("Cannot call user-defined function from filter without interpreter context")
            result = predicate.interpreter._call_function_with_value(predicate, elem)
        elif isinstance(predicate, BuiltinFunction):
            result = predicate.func(elem, space, metric)
        
        # Check if result is truthy
        # Decode the result to determine truthiness
        decoded = decode_vector(result, space, metric)
        
        # Consider truthy: non-zero numbers, non-empty strings, non-null
        is_truthy = False
        if isinstance(decoded, (int, float)):
            is_truthy = decoded != 0
        elif isinstance(decoded, str):
            is_truthy = decoded != "" and decoded != "null"
        elif isinstance(decoded, list):
            is_truthy = len(decoded) > 0
        
        if is_truthy:
            result_elements.append(elem)
    
    return EigenList(result_elements)


def builtin_reduce(args, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Fold/accumulate a list into a single value using a binary function.
    
    Reduce applies a binary function cumulatively to the elements of a list,
    from left to right, reducing the list to a single value. The function should
    accept two arguments: the accumulator and the current element.
    
    Example:
        define add as:
            # Expects a two-element list [a, b]
            a is arg[0]
            b is arg[1]
            return a + b
        
        numbers is [1, 2, 3, 4, 5]
        sum is reduce of [add, numbers, 0]
        # sum = 15 (0+1+2+3+4+5)
    
    Args:
        args: Three-element list [function, target_list, initial_value]
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        The accumulated result as an LRVM vector
    """
    from eigenscript.evaluator.interpreter import EigenList, Function, BuiltinFunction
    
    # Expect args to be an EigenList with 3 elements: [function, list, initial]
    if not isinstance(args, EigenList):
        raise TypeError("reduce requires a function, list, and initial value")
    
    if len(args.elements) != 3:
        raise TypeError("reduce requires exactly 3 arguments: function, list, and initial value")
    
    func = args.elements[0]
    target_list = args.elements[1]
    accumulator = args.elements[2]
    
    # Function must be a Function or BuiltinFunction object
    if not isinstance(func, (Function, BuiltinFunction)):
        raise TypeError("First argument to reduce must be a function")
    
    # Second argument must be an EigenList
    if not isinstance(target_list, EigenList):
        raise TypeError("Second argument to reduce must be a list")
    
    # Apply the function cumulatively
    for elem in target_list.elements:
        # Create a list [accumulator, elem] to pass to the function
        pair = EigenList([accumulator, elem])
        
        # Call the function with the pair
        if isinstance(func, Function):
            # Use the interpreter stored in the function
            if func.interpreter is None:
                raise RuntimeError("Cannot call user-defined function from reduce without interpreter context")
            accumulator = func.interpreter._call_function_with_value(func, pair)
        elif isinstance(func, BuiltinFunction):
            accumulator = func.func(pair, space, metric)
    
    return accumulator


def builtin_sqrt(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the square root of a number.
    
    Example:
        sqrt of 16  -> 4.0
        sqrt of 2   -> 1.414...
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Square root as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        if decoded < 0:
            raise ValueError("sqrt requires a non-negative number")
        return space.embed(math.sqrt(decoded))
    else:
        raise TypeError("sqrt requires a number argument")


def builtin_abs(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the absolute value of a number.
    
    Example:
        abs of -5   -> 5
        abs of 3.14 -> 3.14
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Absolute value as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(abs(decoded))
    else:
        raise TypeError("abs requires a number argument")


def builtin_pow(args, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Raise a number to a power.
    
    Example:
        pow of [2, 3]   -> 8 (2^3)
        pow of [10, 2]  -> 100 (10^2)
    
    Args:
        args: Two-element list [base, exponent]
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Result of base^exponent as LRVM vector
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    if not isinstance(args, EigenList):
        raise TypeError("pow requires a list of [base, exponent]")
    
    if len(args.elements) != 2:
        raise TypeError("pow requires exactly 2 arguments: base and exponent")
    
    base = decode_vector(args.elements[0], space, metric)
    exponent = decode_vector(args.elements[1], space, metric)
    
    if isinstance(base, (int, float)) and isinstance(exponent, (int, float)):
        return space.embed(math.pow(base, exponent))
    else:
        raise TypeError("pow requires numeric arguments")


def builtin_log(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the natural logarithm (base e) of a number.
    
    Example:
        log of 2.718281828  -> 1.0
        log of 1            -> 0.0
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Natural logarithm as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        if decoded <= 0:
            raise ValueError("log requires a positive number")
        return space.embed(math.log(decoded))
    else:
        raise TypeError("log requires a number argument")


def builtin_exp(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate e raised to the power of a number.
    
    Example:
        exp of 0  -> 1.0
        exp of 1  -> 2.718...
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        e^x as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(math.exp(decoded))
    else:
        raise TypeError("exp requires a number argument")


def builtin_sin(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the sine of an angle in radians.
    
    Example:
        sin of 0     -> 0.0
        sin of 1.570 -> 1.0 (approximately π/2)
    
    Args:
        arg: Angle in radians as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Sine as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(math.sin(decoded))
    else:
        raise TypeError("sin requires a number argument")


def builtin_cos(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the cosine of an angle in radians.
    
    Example:
        cos of 0     -> 1.0
        cos of 3.141 -> -1.0 (approximately π)
    
    Args:
        arg: Angle in radians as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Cosine as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(math.cos(decoded))
    else:
        raise TypeError("cos requires a number argument")


def builtin_tan(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Calculate the tangent of an angle in radians.
    
    Example:
        tan of 0     -> 0.0
        tan of 0.785 -> 1.0 (approximately π/4)
    
    Args:
        arg: Angle in radians as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Tangent as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(math.tan(decoded))
    else:
        raise TypeError("tan requires a number argument")


def builtin_floor(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Round a number down to the nearest integer.
    
    Example:
        floor of 3.7  -> 3
        floor of -2.3 -> -3
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Floor as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(float(math.floor(decoded)))
    else:
        raise TypeError("floor requires a number argument")


def builtin_ceil(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Round a number up to the nearest integer.
    
    Example:
        ceil of 3.2  -> 4
        ceil of -2.7 -> -2
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Ceiling as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(float(math.ceil(decoded)))
    else:
        raise TypeError("ceil requires a number argument")


def builtin_round(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Round a number to the nearest integer.
    
    Example:
        round of 3.5  -> 4
        round of 3.4  -> 3
    
    Args:
        arg: Number as LRVM vector
        space: LRVM space for operations
        metric: Metric tensor (optional)
        
    Returns:
        Rounded value as LRVM vector
    """
    decoded = decode_vector(arg, space, metric)
    
    if isinstance(decoded, (int, float)):
        return space.embed(float(round(decoded)))
    else:
        raise TypeError("round requires a number argument")


def get_builtins(space: LRVMSpace) -> dict:
    """
    Get all built-in functions for the EigenScript environment.
    
    Args:
        space: LRVM space for the interpreter
        
    Returns:
        Dictionary mapping function names to BuiltinFunction objects
    """
    builtins = {
        "print": BuiltinFunction(
            name="print",
            func=builtin_print,
            description="Print a value to stdout"
        ),
        "input": BuiltinFunction(
            name="input",
            func=builtin_input,
            description="Read a line from stdin"
        ),
        "len": BuiltinFunction(
            name="len",
            func=builtin_len,
            description="Get the length/magnitude of a value"
        ),
        "type": BuiltinFunction(
            name="type",
            func=builtin_type,
            description="Get the type of a value"
        ),
        "norm": BuiltinFunction(
            name="norm",
            func=builtin_norm,
            description="Get the geometric norm of a vector"
        ),
        "range": BuiltinFunction(
            name="range",
            func=builtin_range,
            description="Generate a range of numbers"
        ),
        "upper": BuiltinFunction(
            name="upper",
            func=builtin_upper,
            description="Convert string to uppercase"
        ),
        "lower": BuiltinFunction(
            name="lower",
            func=builtin_lower,
            description="Convert string to lowercase"
        ),
        "split": BuiltinFunction(
            name="split",
            func=builtin_split,
            description="Split string into list of words"
        ),
        "join": BuiltinFunction(
            name="join",
            func=builtin_join,
            description="Join list of strings into a single string"
        ),
        "append": BuiltinFunction(
            name="append",
            func=builtin_append,
            description="Append an element to a list"
        ),
        "pop": BuiltinFunction(
            name="pop",
            func=builtin_pop,
            description="Remove and return the last element from a list"
        ),
        "min": BuiltinFunction(
            name="min",
            func=builtin_min,
            description="Find the minimum value in a list"
        ),
        "max": BuiltinFunction(
            name="max",
            func=builtin_max,
            description="Find the maximum value in a list"
        ),
        "sort": BuiltinFunction(
            name="sort",
            func=builtin_sort,
            description="Sort a list in ascending order"
        ),
        "map": BuiltinFunction(
            name="map",
            func=builtin_map,
            description="Transform each element in a list using a function"
        ),
        "filter": BuiltinFunction(
            name="filter",
            func=builtin_filter,
            description="Select elements matching criteria"
        ),
        "reduce": BuiltinFunction(
            name="reduce",
            func=builtin_reduce,
            description="Fold/accumulate values with a function"
        ),
        "sqrt": BuiltinFunction(
            name="sqrt",
            func=builtin_sqrt,
            description="Calculate the square root of a number"
        ),
        "abs": BuiltinFunction(
            name="abs",
            func=builtin_abs,
            description="Calculate the absolute value of a number"
        ),
        "pow": BuiltinFunction(
            name="pow",
            func=builtin_pow,
            description="Raise a number to a power"
        ),
        "log": BuiltinFunction(
            name="log",
            func=builtin_log,
            description="Calculate the natural logarithm"
        ),
        "exp": BuiltinFunction(
            name="exp",
            func=builtin_exp,
            description="Calculate e raised to a power"
        ),
        "sin": BuiltinFunction(
            name="sin",
            func=builtin_sin,
            description="Calculate the sine of an angle in radians"
        ),
        "cos": BuiltinFunction(
            name="cos",
            func=builtin_cos,
            description="Calculate the cosine of an angle in radians"
        ),
        "tan": BuiltinFunction(
            name="tan",
            func=builtin_tan,
            description="Calculate the tangent of an angle in radians"
        ),
        "floor": BuiltinFunction(
            name="floor",
            func=builtin_floor,
            description="Round a number down to the nearest integer"
        ),
        "ceil": BuiltinFunction(
            name="ceil",
            func=builtin_ceil,
            description="Round a number up to the nearest integer"
        ),
        "round": BuiltinFunction(
            name="round",
            func=builtin_round,
            description="Round a number to the nearest integer"
        ),
    }
    
    return builtins
