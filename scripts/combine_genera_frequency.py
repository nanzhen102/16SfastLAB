"""
loops over *_blastn_ssu_r220_Lac_genus_Lactobacillaceae_genera_frequency.csv
extracts the sample name and the “genus” along with its “relative_abundance_%” value
creates a combined CSV file where the row indices are a fixed list of genera

python combine_genera_frequency.py <input_folder> <output_csv>
"""

#!/usr/bin/env python3
import os
import glob
import pandas as pd
import sys

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python python combine_genera_frequency.py <input_folder> <output_csv>")
    
    input_folder = sys.argv[1]
    output_csv = sys.argv[2]
    
    genera_list = [
        "Lactobacillus",
        "Amylolactobacillus",
        "Holzapfeliella",
        "Xylocopilactobacillus",
        "Bombilactobacillus",
        "Companilactobacillus",
        "Lapidilactobacillus",
        "Agrilactobacillus",
        "Schleiferilactobacillus",
        "Lacticaseibacillus",
        "Paralactobacillus",
        "Latilactobacillus",
        "Loigolactobacillus",
        "Dellaglioa",
        "Liquorilactobacillus",
        "Ligilactobacillus",
        "Pediococcus",
        "Lactiplantibacillus",
        "Fructilactobacillus",
        "Acetilactobacillus",
        "Philodulcilactobacillus",
        "Nicoliella",
        "Apilactobacillus",
        "Lentilactobacillus",
        "Secundilactobacillus",
        "Levilactobacillus",
        "Paucilactobacillus",
        "Limosilactobacillus",
        "Furfurilactobacillus",
        "Periweissella",
        "Weissella",
        "Oenococcus",
        "Eupransor",
        "Convivina",
        "Fructobacillus",
        "Leuconostoc"
    ]
    
    combined_df = pd.DataFrame(index=genera_list)

    # Get list of all CSV files matching the pattern *_frequency.csv in the input folder.
    files = glob.glob(os.path.join(input_folder, "*_frequency.csv"))
    if not files:
        sys.exit(f"No frequency CSV files found in folder: {input_folder}")
    
    # Process each frequency CSV file.
    for file in files:
        basename = os.path.basename(file)
        # Extract sample name: assume it is the part before the first underscore.
        sample_name = basename.split("_")[0]
        print(f"Processing sample: {sample_name} from file: {basename}")
        
        try:
            df = pd.read_csv(file)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue
        
        # Build a dictionary mapping genus -> relative_abundance_%.
        # We assume the CSV has at least columns "genus" and "relative_abundance_%" (case sensitive)
        sample_dict = {}
        for _, row in df.iterrows():
            genus = row.get("genus")
            try:
                rel_abundance = float(row.get("relative_abundance_%", 0))
            except:
                rel_abundance = 0.0
            if genus:
                sample_dict[genus] = rel_abundance
        
        # For each genus in the fixed list, get the relative abundance if present, else 0.
        sample_values = {genus: sample_dict.get(genus, 0.0) for genus in genera_list}
        # Add this dictionary as a new column to the combined DataFrame.
        combined_df[sample_name] = pd.Series(sample_values)
    
    # Optionally, sort columns by sample name.
    combined_df = combined_df.sort_index(axis=1)
    
    # Format all cell values to exactly two decimal places.
    combined_df = combined_df.applymap(lambda x: f"{x:0.2f}")
    
    # Write the combined DataFrame to the output CSV file.
    combined_df.to_csv(output_csv)
    print(f"\nCombined genera frequency table saved to: {output_csv}")

if __name__ == "__main__":
    main()