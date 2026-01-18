"""Structural Design Pattern: Facade.

Provides a single interface to many algorithm modules.
"""

from __future__ import annotations

from typing import Any, Dict

from algorithms.rsa import (
    PrivateKey,
    decrypt_blocks,
    encrypt_message,
    format_ciphertext,
    generate_keypair,
    parse_ciphertext,
)
from algorithms.fibonacci_dp import fibonacci
from algorithms.selection_sort import selection_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.merge_sort import merge_sort
from algorithms.card_shuffle import create_standard_deck, fisher_yates_shuffle
from algorithms.factorial import factorial
from algorithms.stats_search import describe
from algorithms.palindrome_counter import count_palindrome_substrings


class AlgorithmsFacade:
    def run(self, name: str, params: Dict[str, Any]) -> str:
        name = name.strip()
        if name == "RSA Encrypt/Decrypt":
            return self._run_rsa(params)
        if name == "Fibonacci (DP)":
            n = int(params["n"])
            return f"Fibonacci({n}) = {fibonacci(n)}"
        if name == "Selection Sort":
            return f"Sorted: {selection_sort(params['array'], ascending=params.get('ascending', True))}"
        if name == "Bubble Sort":
            return f"Sorted: {bubble_sort(params['array'], ascending=params.get('ascending', True))}"
        if name == "Merge Sort":
            return f"Sorted: {merge_sort(params['array'], ascending=params.get('ascending', True))}"
        if name == "Shuffle Deck":
            seed = params.get('seed')
            deck = create_standard_deck()
            shuffled = fisher_yates_shuffle(deck, seed=seed)
            return "Shuffled deck order:\n" + ", ".join(shuffled)
        if name == "Factorial (Recursion)":
            n = int(params['n'])
            return f"{n}! = {factorial(n)}"
        if name == "Array Statistics":
            stats = describe(params['array'])
            return (
                "Statistics (from scratch):\n"
                f"Sorted: {stats['sorted']}\n"
                f"Smallest: {stats['smallest']}\n"
                f"Largest: {stats['largest']}\n"
                f"Mode(s): {stats['mode']} (count={stats['mode_count']})\n"
                f"Median: {stats['median']}\n"
                f"Q1: {stats['q1']}\n"
                f"Q3: {stats['q3']}"
            )
        if name == "Palindrome Substrings (DP)":
            s = str(params['text'])
            return f"Number of palindromic substrings in '{s}': {count_palindrome_substrings(s)}"
        raise ValueError(f"Unknown algorithm: {name}")

    def _run_rsa(self, params: Dict[str, Any]) -> str:
        mode = params.get('mode', 'encrypt')
        if mode == 'encrypt':
            message = str(params.get('message', ''))
            p = params.get('p')
            q = params.get('q')
            e = params.get('e')
            p_int = int(p) if p not in (None, '') else None
            q_int = int(q) if q not in (None, '') else None
            e_int = int(e) if e not in (None, '') else None
            kp = generate_keypair(p=p_int, q=q_int, e=e_int)
            blocks = encrypt_message(message, kp.public)
            return (
                "RSA Encryption Result:\n"
                f"Public key (n, e): ({kp.public.n}, {kp.public.e})\n"
                f"Private key (n, d): ({kp.private.n}, {kp.private.d})\n"
                "Ciphertext blocks:\n"
                f"{format_ciphertext(blocks)}\n\n"
                "Tip: copy ciphertext blocks and decrypt using (n, d)."
            )
        if mode == 'decrypt':
            ciphertext = str(params.get('ciphertext', ''))
            n = params.get('n')
            d = params.get('d')
            if n in (None, '') or d in (None, ''):
                raise ValueError('To decrypt, please provide n and d.')
            blocks = parse_ciphertext(ciphertext)
            plaintext = decrypt_blocks(blocks, PrivateKey(n=int(n), d=int(d)))
            return "RSA Decryption Result:\n" + plaintext
        raise ValueError('mode must be encrypt or decrypt')
