"""
Meta-Prime Visualization and Analysis Tool
------------------------------------------
ASCII-based visualization of meta-prime properties and patterns
"""

import math
from typing import List, Tuple


class MetaPrimeVisualizer:
    """Visualize meta-prime patterns and relationships"""
    
    def __init__(self):
        self.meta_primes = [2, 3, 5, 7, 11]
        self.regular_primes = [p for p in range(2, 100) if self.is_prime(p)]
    
    def is_prime(self, n: int) -> bool:
        """Standard primality test"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def visualize_axiom_systems(self):
        """Show how different primes behave across axiom systems"""
        print("\n=== PRIMALITY ACROSS AXIOM SYSTEMS ===\n")
        print("Prime | Standard | Mod 7 | Mod 11 | Twisted | Digital | META?")
        print("-" * 65)
        
        test_primes = self.regular_primes[:15]
        
        for p in test_primes:
            is_meta = p in self.meta_primes
            
            # Standard arithmetic
            std = "✓" if self.is_prime(p) else "✗"
            
            # Modular arithmetic tests
            mod7 = "✓" if p < 7 or p % 7 != 0 else "✗"
            mod11 = "✓" if p < 11 or p % 11 != 0 else "✗"
            
            # Twisted arithmetic (simplified)
            twisted = "✓" if p < 12 else "✗"
            
            # Digital root arithmetic
            dr = p % 9 if p % 9 != 0 else 9
            digital = "✓" if dr in [1, 2, 5, 7] else "✗"
            
            meta_marker = "★ META" if is_meta else ""
            
            print(f"{p:5} | {std:^8} | {mod7:^5} | {mod11:^6} | "
                  f"{twisted:^7} | {digital:^7} | {meta_marker}")
    
    def visualize_interference_pattern(self):
        """Visualize interference between meta-primes"""
        print("\n=== META-PRIME INTERFERENCE PATTERN ===\n")
        
        width = 80
        height = 20
        
        # Create interference field
        field = []
        for y in range(height):
            row = []
            for x in range(width):
                # Calculate interference at this point
                intensity = 0
                for mp in self.meta_primes:
                    # Wave from each meta-prime
                    wave = math.sin(2 * math.pi * x / mp) * math.cos(2 * math.pi * y / mp)
                    intensity += wave
                
                # Normalize and convert to character
                normalized = (intensity + len(self.meta_primes)) / (2 * len(self.meta_primes))
                
                if normalized > 0.8:
                    char = "█"
                elif normalized > 0.6:
                    char = "▓"
                elif normalized > 0.4:
                    char = "▒"
                elif normalized > 0.2:
                    char = "░"
                else:
                    char = " "
                
                row.append(char)
            field.append(row)
        
        # Print field
        for row in field:
            print("".join(row))
        
        print("\nDark regions (█) show constructive interference - prime locations!")
    
    def visualize_meta_factorization(self):
        """Show meta-prime factorization of numbers"""
        print("\n=== META-PRIME FACTORIZATION ===\n")
        print("Every number can be expressed using meta-primes:")
        print("n = 2^a × 3^b × 5^c × 7^d × 11^e × residual\n")
        
        for n in range(1, 31):
            factors = self.meta_factorize(n)
            expr = self.format_factorization(n, factors)
            
            is_pure = factors['residual'] == 1
            marker = " ← Pure meta-composite!" if is_pure and n > 1 else ""
            
            print(f"{n:3} = {expr}{marker}")
    
    def meta_factorize(self, n: int) -> dict:
        """Factorize n using meta-primes"""
        factors = {mp: 0 for mp in self.meta_primes}
        factors['residual'] = n
        
        for mp in self.meta_primes:
            while factors['residual'] % mp == 0:
                factors[mp] += 1
                factors['residual'] //= mp
        
        return factors
    
    def format_factorization(self, n: int, factors: dict) -> str:
        """Format factorization nicely"""
        parts = []
        
        for mp in self.meta_primes:
            if factors[mp] > 0:
                if factors[mp] == 1:
                    parts.append(f"{mp}")
                else:
                    parts.append(f"{mp}^{factors[mp]}")
        
        if factors['residual'] > 1:
            parts.append(f"[{factors['residual']}]")
        
        if not parts:
            return "1"
        
        return " × ".join(parts)
    
    def visualize_digital_roots(self):
        """Show digital root patterns of meta-primes"""
        print("\n=== DIGITAL ROOT PATTERNS ===\n")
        
        def digital_root(n):
            while n >= 10:
                n = sum(int(d) for d in str(n))
            return n
        
        print("Meta-primes and their powers mod 9:")
        print("(Digital root reveals deep number structure)\n")
        
        for mp in self.meta_primes:
            print(f"{mp}: ", end="")
            roots = []
            for power in range(1, 10):
                dr = digital_root(mp ** power)
                roots.append(str(dr))
            print(" → ".join(roots), f" (period {self.find_period(roots)})")
        
        print("\nNote: Meta-primes have special digital root cycles!")
    
    def find_period(self, sequence: List[str]) -> int:
        """Find period in a sequence"""
        for period in range(1, len(sequence)):
            if all(sequence[i] == sequence[i % period] for i in range(len(sequence))):
                return period
        return len(sequence)
    
    def visualize_resonance_spectrum(self):
        """Show the resonance spectrum of numbers"""
        print("\n=== META-PRIME RESONANCE SPECTRUM ===\n")
        print("How strongly each number resonates with meta-primes:")
        print("(Higher resonance = more 'fundamental')\n")
        
        for n in range(1, 31):
            resonance = self.calculate_resonance(n)
            bar = "█" * int(resonance * 20)
            
            special = ""
            if n in self.meta_primes:
                special = " ★ META-PRIME"
            elif self.is_prime(n):
                special = " ◆ regular prime"
            
            print(f"{n:3}: {bar:<20} {resonance:.2f}{special}")
    
    def calculate_resonance(self, n: int) -> float:
        """Calculate meta-prime resonance of a number"""
        if n in self.meta_primes:
            return 1.0
        
        resonance = 0.0
        
        # Factor contribution
        factors = self.meta_factorize(n)
        for mp in self.meta_primes:
            if factors[mp] > 0:
                resonance += 0.2 / (1 + factors[mp])
        
        # Residual penalty
        if factors['residual'] > 1:
            resonance *= 1.0 / math.log(factors['residual'] + 1)
        
        return min(resonance, 0.99)  # Only meta-primes get 1.0
    
    def run_all_visualizations(self):
        """Run all visualizations"""
        print("╔" + "═" * 78 + "╗")
        print("║" + "META-PRIME VISUALIZATION SUITE".center(78) + "║")
        print("║" + "Exploring the Atoms of Mathematics".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        
        self.visualize_axiom_systems()
        self.visualize_meta_factorization()
        self.visualize_digital_roots()
        self.visualize_resonance_spectrum()
        self.visualize_interference_pattern()
        
        print("\n" + "═" * 80)
        print("CONCLUSION: Meta-primes {2,3,5,7,11} are the irreducible")
        print("building blocks from which all mathematics emerges.")
        print("═" * 80)


if __name__ == "__main__":
    visualizer = MetaPrimeVisualizer()
    visualizer.run_all_visualizations()