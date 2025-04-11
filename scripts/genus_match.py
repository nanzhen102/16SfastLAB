"""
reads the BLAST output file, 
extracts the genus information from the FASTA file using Biopython,  
inserts the genus column right after the subject_id column,  
writes the resulting DataFrame to a CSV file

python genus_match.py <blast_output_file> <fna_DB_file> <output_file>
"""

#!/usr/bin/env python3
from Bio import SeqIO
import pandas as pd
import re
import sys

if len(sys.argv) != 4:
    sys.exit("Usage: python genus_match.py <blast_output_file> <fna_DB_file> <output_file>")

blast_output_path = sys.argv[1]
fna_DB_file_path = sys.argv[2]
output_file_path = sys.argv[3]

# Define column names for the BLAST output file
col_names = [
    "query_id", "subject_id", "%identity", "alignment_length", "mismatches",
    "gap_opens", "q_start", "q_end", "s_start", "s_end", "evalue", "bit_score"
]

# Read the BLAST output file (assuming tab-separated values)
blast_df = pd.read_csv(blast_output_path, sep='\t', header=None, names=col_names)

# Create a dictionary to map sequence id to genus (and family, if needed)
seq_info = {}
for record in SeqIO.parse(fna_DB_file_path, "fasta"):
    seq_id = record.id
    description = record.description
    # Use regex to extract genus from description, e.g. "g__Ligilactobacillus"
    genus_match = re.search(r"g__([\w\-]+)", description)
    genus = genus_match.group(1) if genus_match else None
    # Optionally extract family if required in the future
    family_match = re.search(r"f__([\w\-]+)", description)
    family = family_match.group(1) if family_match else None
    
    if genus:
        seq_info[seq_id] = {"genus": genus, "family": family}

# Helper functions to get the genus for a given subject_id
def extract_genus(subject_id):
    return seq_info.get(subject_id, {}).get("genus", None)

# Add the genus column to the BLAST dataframe
blast_df["genus"] = blast_df["subject_id"].apply(extract_genus)

# Since you know all entries are from Lactobacillaceae,
# we skip filtering and simply remove any extra columns if necessary.
# In this case, we only output the desired columns in the correct order.
ordered_columns = [
    "query_id", "subject_id", "genus",
    "%identity", "alignment_length", "mismatches", "gap_opens",
    "q_start", "q_end", "s_start", "s_end", "evalue", "bit_score"
]
final_df = blast_df[ordered_columns]

# Save the resulting DataFrame to a CSV file.
final_df.to_csv(output_file_path, index=False)
print(f"Processed BLAST output with genus column has been saved to {output_file_path}")