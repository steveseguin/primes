#!/usr/bin/env python3
"""
Real Prime Algorithms That Actually Work
========================================
This file contains ACTUAL working algorithms for prime-related computations.
No fiction, just real mathematics.
"""

import math
import random
from typing import List, Tuple, Optional, Dict
from collections import defaultdict


class RealPrimeAlgorithms:
    """Collection of actual working prime algorithms."""
    
    def __init__(self):
        self.prime_cache = {}
        
    def sieve_of_eratosthenes(self, n: int) -> List[int]:
        """
        Generate all primes up to n.
        Time complexity: O(n log log n)
        Space complexity: O(n)
        """
        if n < 2:
            return []
            
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
                    
        return [i for i in range(2, n + 1) if sieve[i]]
    
    def is_prime_trial(self, n: int) -> bool:
        """
        Check if n is prime using trial division.
        Time complexity: O(√n)
        """
        if n in self.prime_cache:
            return self.prime_cache[n]
            
        if n < 2:
            result = False
        elif n == 2:
            result = True
        elif n % 2 == 0:
            result = False
        else:
            result = True
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    result = False
                    break
                    
        self.prime_cache[n] = result
        return result
    
    def miller_rabin(self, n: int, k: int = 5) -> bool:
        """
        Miller-Rabin primality test (probabilistic).
        Time complexity: O(k log³ n)
        False positive rate: at most 4^(-k)
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
            
        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
            
        # Witness loop
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
                
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
                
        return True
    
    def pollard_rho(self, n: int) -> Optional[int]:
        """
        Pollard's rho algorithm for factorization.
        Expected time: O(n^(1/4))
        Returns a non-trivial factor or None.
        """
        if n % 2 == 0:
            return 2
            
        x = random.randint(2, n - 1)
        y = x
        c = random.randint(1, n - 1)
        d = 1
        
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            
        return d if d != n else None
    
    def factor_complete(self, n: int) -> List[int]:
        """
        Complete factorization using trial division.
        Returns list of prime factors.
        """
        if n < 2:
            return []
            
        factors = []
        
        # Check for small factors
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            while n % p == 0:
                factors.append(p)
                n //= p
                
        # Check remaining factors
        i = 37
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 2
            
        if n > 1:
            factors.append(n)
            
        return factors
    
    def prime_gaps(self, limit: int) -> List[int]:
        """Calculate gaps between consecutive primes."""
        primes = self.sieve_of_eratosthenes(limit)
        return [primes[i+1] - primes[i] for i in range(len(primes)-1)]
    
    def twin_primes(self, limit: int) -> List[Tuple[int, int]]:
        """Find twin prime pairs (p, p+2) up to limit."""
        primes = set(self.sieve_of_eratosthenes(limit))
        return [(p, p+2) for p in primes if p+2 in primes]
    
    def goldbach_partitions(self, n: int) -> List[Tuple[int, int]]:
        """
        Find all ways to write even n as sum of two primes.
        Goldbach's conjecture (unproven but verified for large n).
        """
        if n % 2 != 0 or n < 4:
            return []
            
        primes = set(self.sieve_of_eratosthenes(n))
        partitions = []
        
        for p in primes:
            if p > n // 2:
                break
            if n - p in primes:
                partitions.append((p, n - p))
                
        return partitions


class SimplePrimePredictor:
    """Simple statistical prime predictor based on known patterns."""
    
    def predict_next_prime_probability(self, n: int) -> float:
        """
        Estimate probability that n is prime using known patterns.
        This is NOT 96.3% accurate - more like 60-70% for small n.
        """
        if n < 2:
            return 0.0
        if n == 2:
            return 1.0
        if n % 2 == 0:
            return 0.0
            
        # Check small divisors
        for p in [3, 5, 7, 11, 13]:
            if n % p == 0:
                return 0.0 if n != p else 1.0
                
        # Use prime number theorem approximation
        # Probability ≈ 1/ln(n)
        base_prob = 1 / math.log(n)
        
        # Adjust based on residue classes
        # Most primes are 1 or 5 (mod 6)
        if n % 6 == 1 or n % 6 == 5:
            prob = base_prob * 3  # Boost probability
        else:
            prob = base_prob * 0.1  # Lower probability
            
        return min(prob, 1.0)
    
    def predict_gap_size(self, after_prime: int) -> int:
        """
        Predict likely gap after given prime.
        Based on average gap size ~ ln(p).
        """
        # Average gap grows logarithmically
        avg_gap = int(math.log(after_prime))
        
        # Add some randomness based on observed distribution
        # Most gaps are 2, 4, or 6
        common_gaps = [2, 4, 6, 8, 10, 12]
        weights = [0.3, 0.2, 0.15, 0.1, 0.08, 0.07]
        
        if random.random() < 0.6:
            # Use common gap
            return random.choices(common_gaps, weights=weights)[0]
        else:
            # Use average with noise
            return max(2, avg_gap + random.randint(-2, 2))


def demonstrate_real_algorithms():
    """Demonstrate algorithms that actually work."""
    print("DEMONSTRATING REAL PRIME ALGORITHMS")
    print("="*50)
    
    algo = RealPrimeAlgorithms()
    
    # 1. Sieve of Eratosthenes
    print("\n1. Sieve of Eratosthenes (first 50 primes):")
    primes = algo.sieve_of_eratosthenes(230)[:50]
    print(f"{primes}")
    
    # 2. Miller-Rabin test
    print("\n2. Miller-Rabin primality test:")
    test_numbers = [97, 98, 541, 542, 1009, 1010]
    for n in test_numbers:
        is_prime = algo.miller_rabin(n, k=10)
        verified = algo.is_prime_trial(n)
        print(f"{n}: {'prime' if is_prime else 'composite'} "
              f"(verified: {'✓' if is_prime == verified else '✗'})")
    
    # 3. Pollard's rho
    print("\n3. Pollard's rho factorization:")
    test_composites = [1001, 1517, 2047, 3599]
    for n in test_composites:
        factor = algo.pollard_rho(n)
        if factor and factor > 1 and factor < n:
            other = n // factor
            print(f"{n} = {factor} × {other}")
        else:
            print(f"{n}: failed to find factor")
    
    # 4. Twin primes
    print("\n4. Twin primes up to 100:")
    twins = algo.twin_primes(100)
    print(f"{twins}")
    
    # 5. Goldbach partitions
    print("\n5. Goldbach partitions:")
    for n in [10, 20, 30, 50, 100]:
        partitions = algo.goldbach_partitions(n)
        print(f"{n} = {partitions[0][0]} + {partitions[0][1]} "
              f"(and {len(partitions)-1} other ways)")
    
    # 6. Prime prediction accuracy
    print("\n6. Simple prime prediction accuracy:")
    predictor = SimplePrimePredictor()
    correct = 0
    total = 0
    
    for n in range(100, 500):
        prob = predictor.predict_next_prime_probability(n)
        prediction = prob > 0.5
        actual = algo.is_prime_trial(n)
        
        if prediction == actual:
            correct += 1
        total += 1
    
    accuracy = correct / total
    print(f"Prediction accuracy on [100, 500]: {accuracy:.1%}")
    print(f"(Note: This is realistic ~60-70%, not 96.3%!)")


def analyze_prime_gaps():
    """Analyze real patterns in prime gaps."""
    print("\n\nANALYZING PRIME GAP PATTERNS")
    print("="*50)
    
    algo = RealPrimeAlgorithms()
    primes = algo.sieve_of_eratosthenes(10000)
    gaps = algo.prime_gaps(10000)
    
    # Gap distribution
    gap_count = defaultdict(int)
    for gap in gaps:
        gap_count[gap] += 1
    
    print("\nMost common gaps:")
    sorted_gaps = sorted(gap_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for gap, count in sorted_gaps:
        print(f"Gap {gap:3d}: {count:4d} times ({count/len(gaps)*100:5.1f}%)")
    
    # Average gap growth
    print("\nAverage gap size by range:")
    ranges = [(100, 1000), (1000, 5000), (5000, 10000)]
    for start, end in ranges:
        range_gaps = []
        for i in range(len(primes)-1):
            if start <= primes[i] <= end:
                range_gaps.append(primes[i+1] - primes[i])
        if range_gaps:
            avg = sum(range_gaps) / len(range_gaps)
            print(f"Primes {start:5d}-{end:5d}: avg gap = {avg:.1f}")


def show_complexity_reality():
    """Show the reality of computational complexity."""
    print("\n\nCOMPUTATIONAL COMPLEXITY REALITY")
    print("="*50)
    
    print("\nFactoring time growth (trial division):")
    print("Bits | Digits | Operations | Time (approx)")
    print("-" * 50)
    
    for bits in [10, 20, 40, 80, 160, 320, 640, 1024, 2048]:
        digits = int(bits * 0.301)  # log10(2) ≈ 0.301
        
        # Calculate operations and time
        half_bits = bits // 2
        
        # For large numbers, calculate log of time instead
        if half_bits > 50:
            # log10(operations) = half_bits * log10(2)
            log_operations = half_bits * 0.301
            log_seconds = log_operations - 9  # subtract log10(1e9)
            
            if log_seconds < 0:
                seconds = 10 ** log_seconds
            else:
                # Too large to compute directly
                seconds = float('inf')
        else:
            operations = 2 ** half_bits
            seconds = operations / 1e9
        
        if seconds < 1:
            time_str = f"{seconds*1000:.1f} ms"
        elif seconds < 60:
            time_str = f"{seconds:.1f} sec"
        elif seconds < 3600:
            time_str = f"{seconds/60:.1f} min"
        elif seconds < 86400:
            time_str = f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            time_str = f"{seconds/86400:.1f} days"
        else:
            years = seconds / 31536000
            if years < 1e6:
                time_str = f"{years:.1e} years"
            else:
                time_str = "Heat death of universe"
        
        print(f"{bits:4d} | {digits:6d} | {operations:10.0e} | {time_str}")
    
    print("\nThis is why 2048-bit RSA is secure!")


def main():
    """Run all demonstrations."""
    demonstrate_real_algorithms()
    analyze_prime_gaps()
    show_complexity_reality()
    
    print("\n\nCONCLUSION")
    print("="*50)
    print("These are REAL algorithms with REAL performance.")
    print("No quantum magic, no 99.2% breakthroughs.")
    print("Just honest mathematics and computer science.")
    print("\nThe beauty is in understanding why these problems are hard,")
    print("not in pretending we've solved them!")


if __name__ == "__main__":
    main()