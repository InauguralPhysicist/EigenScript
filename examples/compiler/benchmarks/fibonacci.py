#!/usr/bin/env python3
"""Fibonacci benchmark - Python baseline"""

def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)

x = fib(25)
print(x)
