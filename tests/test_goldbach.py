import math
import unittest

from real_prime_algorithms import RealPrimeAlgorithms


def is_prime_reference(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


class GoldbachPartitionsTests(unittest.TestCase):
    def setUp(self):
        self.algorithms = RealPrimeAlgorithms()

    def test_set_iteration_order_must_not_skip_small_primes(self):
        self.assertEqual(self.algorithms.goldbach_partitions(38), [(7, 31), (19, 19)])

    def test_demonstration_input_returns_all_partitions(self):
        self.assertEqual(self.algorithms.goldbach_partitions(50),
                         [(3, 47), (7, 43), (13, 37), (19, 31)])

    def test_even_inputs_match_independent_trial_division(self):
        for n in range(4, 1001, 2):
            with self.subTest(n=n):
                expected = [(p, n - p) for p in range(2, n // 2 + 1)
                            if is_prime_reference(p) and is_prime_reference(n - p)]
                self.assertEqual(self.algorithms.goldbach_partitions(n), expected)

    def test_invalid_and_small_inputs(self):
        for n in [-10, 0, 1, 2, 3, 5, 99]:
            with self.subTest(n=n):
                self.assertEqual(self.algorithms.goldbach_partitions(n), [])
        self.assertEqual(self.algorithms.goldbach_partitions(4), [(2, 2)])
        self.assertEqual(self.algorithms.goldbach_partitions(6), [(3, 3)])


if __name__ == '__main__':
    unittest.main()
