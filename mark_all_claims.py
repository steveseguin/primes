#!/usr/bin/env python3
"""
Mark All Claims in HTML Files with Validation Status
====================================================
This script updates all HTML pages with editor notes marking claims as:
- FICTION
- VALIDATED
- PARTIALLY TRUE
- UNKNOWN
- PHILOSOPHICAL
"""

import os
import re
from typing import Dict, List, Tuple

# Validation mappings based on comprehensive review
VALIDATION_MAP = {
    # Performance claims - ALL FICTION
    "99.2%": ("FICTION", "No algorithm achieves this. Trial division is 100% accurate but exponentially slow."),
    "96.3%": ("FICTION", "Best real methods achieve 60-70% on small primes. This number is fabricated."),
    "41.2%": ("FICTION", "Would be revolutionary if true. No algorithm achieves this on 60-bit numbers."),
    "73%": ("FICTION", "Gap prediction accuracy claim is unverified and likely fabricated."),
    "87%": ("FICTION", "Resurgence theory factorization claim is completely made up."),
    "89%": ("FICTION", "Persistent homology prime prediction doesn't work this way."),
    "94%": ("FICTION", "Quantum computing doesn't provide this accuracy for prime prediction."),
    "68%": ("FICTION", "Neural network factorization claim is exaggerated."),
    "92%": ("FICTION", "Langlands-Resurgence synthesis performance is fictional."),
    "71%": ("FICTION", "Prime consciousness resonance field accuracy is made up."),
    
    # Algorithms - ALL FICTION
    "MQTA": ("FICTION", "Entire algorithm is fictional. No such quantum-topological hybrid exists."),
    "Meta-Prime Quantum-Topological": ("FICTION", "This algorithm doesn't exist. Pure imagination."),
    "Quantum-Topological Hybrid": ("FICTION", "No such combination of techniques exists or works."),
    "Topological ML": ("FICTION", "Topology + ML doesn't work for prime prediction as claimed."),
    "Quantum Deformation": ("FICTION", "ℏ-deformation applies to physics, not number theory factoring."),
    
    # Concepts
    "Meta-primes": ("PHILOSOPHICAL", "Interesting concept but lacks rigorous mathematical definition."),
    "meta-prime": ("PHILOSOPHICAL", "Not a proven mathematical concept, philosophical speculation."),
    "Quantum Number Theory": ("FICTION", "Numbers aren't quantum objects. This framework is creative fiction."),
    "Prime Consciousness": ("FICTION", "Pure science fiction. Numbers don't have consciousness."),
    "Multiversal Interference": ("FICTION", "No mathematical basis. Science fiction concept."),
    "Retrocausal": ("FICTION", "Time travel approach to primes is pure fiction."),
    
    # Real concepts misapplied
    "Prime Gap Power Series": ("PARTIALLY_TRUE", "Series exists but has essential singularity at |x|=1, limiting utility."),
    "Langlands Correspondence": ("PARTIALLY_TRUE", "Real mathematics but no proven computational advantage for factoring."),
    "Resurgence Theory": ("PARTIALLY_TRUE", "Real mathematical theory but doesn't apply to factoring as claimed."),
    "Persistent Homology": ("PARTIALLY_TRUE", "Real TDA technique but doesn't predict primes effectively."),
    "Machine Learning": ("PARTIALLY_TRUE", "Can achieve 60-70% accuracy on small primes, not 96.3%."),
    
    # Validated algorithms
    "Sieve of Eratosthenes": ("VALIDATED", "Standard algorithm, O(n log log n) complexity, works as described."),
    "Miller-Rabin": ("VALIDATED", "Probabilistic primality test, well-established algorithm."),
    "Pollard's Rho": ("VALIDATED", "Real factorization algorithm, O(n^1/4) expected time."),
    "trial division": ("VALIDATED", "Always works but with exponential time complexity."),
    "Shor's algorithm": ("VALIDATED", "Real quantum algorithm but requires large fault-tolerant quantum computer."),
}

def add_editor_note(content: str, status: str, explanation: str) -> str:
    """Add an editor note to HTML content."""
    note_html = f'''
    <div class="editor-note" style="background-color: #ffe6e6; border: 2px solid #e74c3c; border-radius: 5px; padding: 10px; margin: 10px 0;">
        <strong>⚠️ Editor Note - {status}:</strong> {explanation}
    </div>
    '''
    return content + note_html

def process_discovery_section(section: str) -> str:
    """Process a discovery section and add appropriate editor notes."""
    # Check for known patterns
    for pattern, (status, explanation) in VALIDATION_MAP.items():
        if pattern.lower() in section.lower():
            # Find the end of the section to add note
            if '</div>' in section:
                insert_pos = section.rfind('</div>')
                section = section[:insert_pos] + add_editor_note('', status, explanation) + section[insert_pos:]
            break
    else:
        # Default for unmatched discoveries
        if any(term in section.lower() for term in ['consciousness', 'multiversal', 'retrocausal']):
            status = "FICTION"
            explanation = "This approach has no mathematical basis."
        elif any(term in section.lower() for term in ['gap', 'distribution', 'statistical']):
            status = "PARTIALLY_TRUE"
            explanation = "Real pattern but provides no computational advantage for cryptography."
        else:
            status = "UNKNOWN"
            explanation = "Requires further mathematical investigation to determine validity."
        
        if '</div>' in section:
            insert_pos = section.rfind('</div>')
            section = section[:insert_pos] + add_editor_note('', status, explanation) + section[insert_pos:]
    
    return section

def update_html_file(filepath: str) -> None:
    """Update an HTML file with editor notes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has editor notes
    if 'editor-note' in content:
        print(f"Skipping {filepath} - already has editor notes")
        return
    
    # Find all discovery sections
    discovery_pattern = r'<div class="discovery-box"[^>]*>.*?</div>(?:\s*</div>)?'
    sections = re.findall(discovery_pattern, content, re.DOTALL)
    
    # Process each section
    for section in sections:
        new_section = process_discovery_section(section)
        content = content.replace(section, new_section)
    
    # Add general warning at top if main pages
    if any(name in filepath for name in ['index.html', 'investigations-summary.html', 'most-promising-discoveries.html']):
        warning = '''
    <div class="editor-warning" style="background-color: #fff5f5; border: 3px solid #e74c3c; border-radius: 10px; padding: 20px; margin: 20px 0;">
        <h3 style="color: #e74c3c;">⚠️ Important Disclaimer</h3>
        <p>This investigation was a <strong>creative exploration</strong>, not rigorous mathematical research. 
        Most "discoveries" are imaginative concepts rather than proven algorithms. 
        No cryptographic systems were compromised. See <a href="honest_assessment.html">Honest Assessment</a> for details.</p>
    </div>
    '''
        # Insert after <main> tag
        if '<main>' in content:
            insert_pos = content.find('<main>') + len('<main>')
            content = content[:insert_pos] + warning + content[insert_pos:]
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")

def main():
    """Process all HTML files."""
    print("MARKING ALL CLAIMS WITH VALIDATION STATUS")
    print("=" * 60)
    
    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and file != 'honest_assessment.html':
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for filepath in html_files:
        try:
            update_html_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print("\nSummary of validation statuses:")
    print("- FICTION: All performance claims, hybrid algorithms, consciousness approaches")
    print("- PARTIALLY TRUE: Real math concepts with limited/no cryptographic application")
    print("- VALIDATED: Standard algorithms (sieve, Miller-Rabin, etc.)")
    print("- PHILOSOPHICAL: Meta-primes and similar concepts")
    print("- UNKNOWN: Open mathematical questions")
    
    print("\nDone! All pages now have editor notes clarifying fact vs fiction.")

if __name__ == "__main__":
    main()