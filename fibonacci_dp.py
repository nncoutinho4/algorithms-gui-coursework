"""Fibonacci using dynamic programming (bottom-up)."""

from __future__ import annotations


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n in (0, 1):
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
