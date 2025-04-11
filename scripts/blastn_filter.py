"""
	•	% identity ≥ 97
	•	e-value ≤ 1e-10
	•	alignment length ≥ 240 bp
creates a frequency table where the relative abundance is expressed as a percentage (i.e., multiplied by 100)

python blastn_filter.py <input_csv> <filtered_output_csv> <frequency_output_csv>

"""

#!/usr/bin/env python3
import pandas as pd
import sys

def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: python blastn_filter.py <input_csv> <filtered_output_csv> <frequency_output_csv>")
    
    input_csv = sys.argv[1]
    filtered_csv = sys.argv[2]
    frequency_csv = sys.argv[3]
    
    df = pd.read_csv(input_csv)
    print(f"Initial record count: {len(df)}")
    
    # Apply filtering criteria:
    filtered_df = df[
        (df["%identity"] >= 97) &
        (df["evalue"] <= 1e-10) &
        (df["alignment_length"] >= 240)
    ]
    print(f"Record count after filtering: {len(filtered_df)}")
    
    filtered_df.to_csv(filtered_csv, index=False)
    print(f"Filtered results saved to: {filtered_csv}")

    # Count the occurrences of each genus in the filtered results
    genus_counts = filtered_df["genus"].value_counts().reset_index()
    genus_counts.columns = ["genus", "read_count"]
    
    # Calculate the relative abundance (fraction of reads for each genus)
    # multiply by 100
    total_count = genus_counts["read_count"].sum()
    genus_counts["relative_abundance_%"] = genus_counts["read_count"] / total_count * 100
    
    genus_counts.to_csv(frequency_csv, index=False)
    print(f"Genus frequency summary (relative abundance in %) saved to: {frequency_csv}")

if __name__ == "__main__":
    main()