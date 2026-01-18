"""RSA algorithm implemented from scratch (educational).

This module provides:
- Key generation (with a simple primality test)
- Encryption / decryption of text messages

Security note:
Real RSA uses very large primes and padding schemes (e.g., OAEP). This coursework
implementation intentionally keeps numbers small and focuses on the algorithmic steps.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional, Tuple


def gcd(a: int, b: int) -> int:
    """Greatest common divisor (Euclid)."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm.

    Returns (g, x, y) such that ax + by = g = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def modinv(a: int, m: int) -> int:
    """Modular inverse of a modulo m, if it exists."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def modexp(base: int, exponent: int, modulus: int) -> int:
    """Fast modular exponentiation (square-and-multiply)."""
    if modulus == 1:
        return 0
    result = 1
    base %= modulus
    e = exponent
    while e > 0:
        if e & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        e >>= 1
    return result


def is_prime(n: int) -> bool:
    """Simple deterministic primality test for small integers."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(low: int = 100, high: int = 400) -> int:
    """Generate a random prime in [low, high]."""
    if low >= high:
        raise ValueError("low must be < high")
    while True:
        candidate = random.randint(low, high)
        if is_prime(candidate):
            return candidate


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    n: int
    d: int


@dataclass(frozen=True)
class KeyPair:
    public: PublicKey
    private: PrivateKey


def generate_keypair(p: Optional[int] = None, q: Optional[int] = None, e: Optional[int] = None) -> KeyPair:
    """Generate an RSA key pair.

    If p and q are not provided, random primes are generated.
    If e is not provided, a common default is selected (65537) if possible,
    otherwise the function searches for a valid e.
    """
    if p is None:
        p = generate_prime()
    if q is None:
        q = generate_prime()
    if p == q:
        q = generate_prime()

    if not is_prime(p) or not is_prime(q):
        raise ValueError("p and q must be prime")

    n = p * q
    phi = (p - 1) * (q - 1)

    if e is None:
        preferred = 65537
        if preferred < phi and gcd(preferred, phi) == 1:
            e = preferred
        else:
            e = 3
            while e < phi and gcd(e, phi) != 1:
                e += 2

    if e <= 1 or e >= phi:
        raise ValueError("e must satisfy 1 < e < phi")
    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime with phi")

    d = modinv(e, phi)
    return KeyPair(public=PublicKey(n=n, e=e), private=PrivateKey(n=n, d=d))


def encrypt_message(message: str, public_key: PublicKey) -> List[int]:
    """Encrypt a string. Output is a list of integers (cipher blocks)."""
    cipher_blocks: List[int] = []
    for ch in message:
        m = ord(ch)
        if m >= public_key.n:
            raise ValueError("Message character code is >= n. Use larger keys.")
        c = modexp(m, public_key.e, public_key.n)
        cipher_blocks.append(c)
    return cipher_blocks


def decrypt_blocks(cipher_blocks: List[int], private_key: PrivateKey) -> str:
    """Decrypt a list of integers back to a string."""
    chars: List[str] = []
    for c in cipher_blocks:
        m = modexp(c, private_key.d, private_key.n)
        chars.append(chr(m))
    return "".join(chars)


def parse_ciphertext(ciphertext: str) -> List[int]:
    """Parse ciphertext like '12 99 104' into a list of integers."""
    text = ciphertext.strip()
    if not text:
        return []
    parts = text.split()
    blocks: List[int] = []
    for p in parts:
        blocks.append(int(p))
    return blocks


def format_ciphertext(blocks: List[int]) -> str:
    return " ".join(str(b) for b in blocks)
