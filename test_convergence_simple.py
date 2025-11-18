#!/usr/bin/env python3
"""Simple convergence test with detailed output."""

from eigenscript.lexer.tokenizer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.evaluator.interpreter import Interpreter

print("Testing convergence detection with instrumentation")
print("=" * 70)

code = """
define self_loop as:
    return self_loop of n

result is self_loop of 1
"""

tokens = Tokenizer(code).tokenize()
ast = Parser(tokens).parse()

# Very low threshold to trigger quickly
interp = Interpreter(
    dimension=768,
    enable_convergence_detection=True,
    convergence_threshold=0.3,  # Very low
    max_iterations=100
)

# Instrument to see what's happening
original_call = interp._call_function_with_value

def instrumented_call(func, arg_value):
    depth = interp.recursion_depth
    fs = interp.fs_tracker.compute_fs()
    print(f"Depth {depth}: FS={fs:.4f}, calling {func.name}")

    if depth > 5:  # Stop after a few calls
        print("Stopping instrumentation")
        raise KeyboardInterrupt("Manual stop for inspection")

    return original_call(func, arg_value)

interp._call_function_with_value = instrumented_call

try:
    result = interp.evaluate(ast)
    result_val = interp.environment.lookup("result")
    print(f"\nResult: {result_val}")
    print(f"Final FS: {interp.get_framework_strength():.4f}")
except KeyboardInterrupt:
    print("\nStopped for inspection")
    print(f"FS at stop: {interp.get_framework_strength():.4f}")
except Exception as e:
    print(f"\nException: {type(e).__name__}: {e}")
    print(f"FS at exception: {interp.get_framework_strength():.4f}")
