"""Factorial using recursion."""

from __future__ import annotations


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)
