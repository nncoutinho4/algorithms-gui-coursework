import unittest

from algorithms.fibonacci_dp import fibonacci
from algorithms.factorial import factorial
from algorithms.selection_sort import selection_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.merge_sort import merge_sort
from algorithms.stats_search import describe
from algorithms.palindrome_counter import count_palindrome_substrings
from algorithms.card_shuffle import create_standard_deck, fisher_yates_shuffle
from algorithms.rsa import generate_keypair, encrypt_message, decrypt_blocks


class TestAlgorithms(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(10), 55)

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)

    def test_sorts(self):
        data = [3, 1, 9, 2]
        self.assertEqual(selection_sort(data), [1, 2, 3, 9])
        self.assertEqual(bubble_sort(data, ascending=False), [9, 3, 2, 1])
        self.assertEqual(merge_sort(data), [1, 2, 3, 9])

    def test_stats(self):
        stats = describe([1, 2, 2, 3, 4])
        self.assertEqual(stats["smallest"], 1)
        self.assertEqual(stats["largest"], 4)
        self.assertEqual(stats["mode"], [2])
        self.assertEqual(stats["median"], 2)

    def test_palindrome_count(self):
        self.assertEqual(count_palindrome_substrings("aaa"), 6)
        self.assertEqual(count_palindrome_substrings("abc"), 3)

    def test_shuffle(self):
        deck = create_standard_deck()
        shuffled = fisher_yates_shuffle(deck, seed=123)
        self.assertEqual(len(shuffled), 52)
        self.assertEqual(sorted(shuffled), sorted(deck))

    def test_rsa_roundtrip(self):
        kp = generate_keypair()
        msg = "Hello"
        blocks = encrypt_message(msg, kp.public)
        out = decrypt_blocks(blocks, kp.private)
        self.assertEqual(out, msg)


if __name__ == "__main__":
    unittest.main()
