#!/usr/bin/env python3
"""
REBASE Parser - Extract restriction enzyme data with IUPAC codes preserved
"""
import re

def reverse_complement(seq):
    """Generate reverse complement of DNA sequence with IUPAC codes"""
    complement_map = {
        'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
        'R': 'Y', 'Y': 'R',  # R(AG) <-> Y(CT)
        'M': 'K', 'K': 'M',  # M(AC) <-> K(GT) 
        'S': 'S',            # S(GC) <-> S(GC)
        'W': 'W',            # W(AT) <-> W(AT)
        'B': 'V', 'V': 'B',  # B(CGT) <-> V(ACG)
        'D': 'H', 'H': 'D',  # D(AGT) <-> H(ACT)
        'N': 'N'             # N(ACGT) <-> N(ACGT)
    }
    return ''.join(complement_map.get(base, base) for base in reversed(seq))

def is_valid_enzyme(enzyme):
    """Filter criteria for useful restriction enzymes"""
    
    # Must have a name
    if not enzyme.get('name'):
        return False
    
    # Skip methylases (names starting with M. or containing methylase keywords)
    name = enzyme.get('name', '')
    if name.startswith('M.') or 'methylase' in name.lower():
        return False
    
    # Must have known recognition sequence (not ? or empty)
    recognition = enzyme.get('recognition', '')
    if not recognition or recognition == '?' or len(recognition) < 3:
        return False
    
    # Must be commercially available (non-empty commercial field)
    commercial = enzyme.get('commercial', '')
    if not commercial.strip():
        return False
    
    return True

def clean_recognition_sequence(seq):
    """Remove cleavage site markers and clean up sequence"""
    if not seq:
        return ""
    
    # Remove cleavage site markers ^ and parenthetical info
    cleaned = seq.replace('^', '')
    
    # Remove anything in parentheses (e.g., "(5/10)")
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    
    # Remove whitespace and convert to uppercase
    cleaned = cleaned.strip().upper()
    
    return cleaned

def parse_rebase_file(filename):
    """Parse REBASE allenz file and extract enzyme records"""
    
    enzymes = []
    current_record = {}
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines and header info
            if not line or line.startswith('REBASE') or line.startswith('=-='):
                continue
                
            # Parse tagged lines <NUMBER>content
            if line.startswith('<') and '>' in line:
                # Extract tag number and content
                tag_end = line.find('>')
                tag_num = line[1:tag_end]
                content = line[tag_end + 1:] if tag_end + 1 < len(line) else ""
                
                # Map tag numbers to fields
                if tag_num == '1':  # Enzyme name
                    current_record['name'] = content
                elif tag_num == '2':  # Prototype
                    current_record['prototype'] = content
                elif tag_num == '5':  # Recognition sequence
                    current_record['recognition'] = content
                elif tag_num == '7':  # Commercial availability
                    current_record['commercial'] = content
                elif tag_num == '8':  # Reference number (end of record)
                    current_record['reference'] = content
                    
                    # End of record - filter and save if valid
                    if is_valid_enzyme(current_record):
                        # Clean up the recognition sequence
                        current_record['recognition'] = clean_recognition_sequence(current_record['recognition'])
                        enzymes.append(current_record.copy())
                    current_record = {}
    
    return enzymes

def create_enzyme_database(enzymes):
    """Create the final enzyme database with IUPAC codes preserved"""
    
    enzyme_db = []
    
    for enzyme in enzymes:
        recognition_seq = enzyme['recognition']
        antisense_seq = reverse_complement(recognition_seq)
        
        enzyme_entry = {
            'enzyme_name': enzyme['name'],
            'recognition_seq_5to3': recognition_seq,
            'antisense_seq_5to3': antisense_seq,
            'prototype': enzyme.get('prototype', ''),
            'commercial_sources': enzyme['commercial']
        }
        enzyme_db.append(enzyme_entry)
    
    return enzyme_db

def write_tsv_output(enzyme_db, filename='enzymes.tsv'):
    """Write the enzyme database to TSV file"""
    
    with open(filename, 'w') as f:
        # Write header
        f.write("enzyme_name\trecognition_seq_5to3\tantisense_seq_5to3\tprototype\tcommercial_sources\n")
        
        # Write data
        for enzyme in enzyme_db:
            f.write(f"{enzyme['enzyme_name']}\t{enzyme['recognition_seq_5to3']}\t{enzyme['antisense_seq_5to3']}\t{enzyme['prototype']}\t{enzyme['commercial_sources']}\n")

def main():
    # Parse and filter enzymes
    enzymes = parse_rebase_file('data/allenz.txt')
    print(f"Found {len(enzymes)} valid commercial restriction enzymes")
    
    # Create database with IUPAC codes preserved
    enzyme_db = create_enzyme_database(enzymes)
    print(f"Created database with {len(enzyme_db)} enzyme entries")
    
    # Write to TSV file
    write_tsv_output(enzyme_db)
    print("Database written to enzymes.tsv")
    
    # Show some examples
    print("\nExample entries:")
    for i, enzyme in enumerate(enzyme_db[:10]):
        print(f"{enzyme['enzyme_name']}: {enzyme['recognition_seq_5to3']} / {enzyme['antisense_seq_5to3']}")
    
    # Show some with ambiguous bases
    print("\nExamples with ambiguous bases:")
    ambiguous_examples = [e for e in enzyme_db if any(c in 'RYMKSWBDHVN' for c in e['recognition_seq_5to3'])][:5]
    for enzyme in ambiguous_examples:
        print(f"{enzyme['enzyme_name']}: {enzyme['recognition_seq_5to3']} / {enzyme['antisense_seq_5to3']}")

if __name__ == "__main__":
    main()
