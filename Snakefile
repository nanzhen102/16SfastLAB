configfile: "config.yaml"

import glob
import os

samples = [os.path.basename(f).replace("_1.fastq.gz", "").replace("_1.fastq", "") for f in glob.glob(os.path.join(config["data_dir"], "*_1.fastq*")) if os.path.basename(f).startswith(("ERR", "SRR"))]

def get_input_ext(sample):
    if os.path.exists(os.path.join(config["data_dir"], f"{sample}_1.fastq.gz")):
        return "fastq.gz"
    elif os.path.exists(os.path.join(config["data_dir"], f"{sample}_1.fastq")):
        return "fastq"
    else:
        raise ValueError(f"Missing input file for sample {sample}")

rule all:
    input:
        os.path.join(config["results_dir"], "combined_genera_frequency.csv")


rule merge_pairs:
    input:
        fwd = lambda wildcards: os.path.join(config["data_dir"], f"{wildcards.sample}_1.{get_input_ext(wildcards.sample)}"),
        rev = lambda wildcards: os.path.join(config["data_dir"], f"{wildcards.sample}_2.{get_input_ext(wildcards.sample)}")
    output:
        os.path.join(config["results_dir"], "{sample}_merged.fastq")
    log:
        os.path.join(config["logs_dir"], "{sample}_merge.log")
    # conda:
    #     "envs/vsearch.yaml"
    shell:
        '''
        echo "Merging sample: {wildcards.sample}" > {log}
        vsearch --fastq_mergepairs {input.fwd} \
                --reverse {input.rev} \
                --fastqout {output} >> {log} 2>&1
        '''

rule fastq_to_fasta:
    input:
        os.path.join(config["results_dir"],"{sample}_merged.fastq")
    output:
        os.path.join(config["results_dir"],"{sample}_merged.fasta")
    log:
        os.path.join(config["logs_dir"],"{sample}_fastq_to_fasta.log")
    # conda:
    #     "envs/vsearch.yaml"
    shell:
        """
        vsearch --fastq_filter {input} \
        --fastaout {output} \
        --fasta_width 0 >> {log} 2>&1
        """

rule blastn:
    input:
        os.path.join(config["results_dir"],"{sample}_merged.fasta")
    output:
        os.path.join(config["results_dir"],"{sample}_blastn_ssu_r220_LAB.out")
    log:
        os.path.join(config["logs_dir"],"{sample}_blastn.log")
    threads:
        config["blast"]["threads"]
    # conda:
    #     "envs/blast.yaml"
    shell:
        """
        blastn -query {input} \
        -db {config[blast_db]} \
        -out {output} \
        -outfmt {config[blast][outfmt]} \
        -evalue {config[blast][evalue]} \
        -max_target_seqs {config[blast][max_target_seqs]} \
        -num_threads {threads} >> {log} 2>&1
        """

rule genus_match:
    input:
        os.path.join(config["results_dir"], "{sample}_blastn_ssu_r220_LAB.out")
    output:
        os.path.join(config["results_dir"], "{sample}_genus_match.csv")
    log:
        os.path.join(config["logs_dir"], "{sample}_genus_match.log")
    # conda:
    #     "envs/python_scripts.yaml"
    shell:
        """
        python {config[scripts_dir]}/genus_match.py {input} {config[fna_file]} {output} 2> {log}
        """

rule blastn_filter:
    input:
        os.path.join(config["results_dir"], "{sample}_genus_match.csv")
    output:
        filtered = os.path.join(config["results_dir"], "{sample}_filtered.csv"),
        frequency = os.path.join(config["results_dir"], "{sample}_frequency.csv")
    log:
        os.path.join(config["logs_dir"], "{sample}_filter.log")
    # conda:
    #     "envs/python_scripts.yaml"
    shell:
        """
        python {config[scripts_dir]}/blastn_filter.py {input} {output.filtered} {output.frequency} 2> {log}
        """

# Dummy flag to ensure combine_genera_frequency runs after all per-sample frequency files are ready.
rule flag:
    input:
        expand(os.path.join(config["results_dir"], "{sample}_frequency.csv"), sample=samples)
    output:
        os.path.join(config["results_dir"], "flag.txt")
    shell:
        "touch {output}"

rule combine_genera_frequency:
    input:
        flag = os.path.join(config["results_dir"], "flag.txt")
    output:
        os.path.join(config["results_dir"], "combined_genera_frequency.csv")
    log:
        os.path.join(config["logs_dir"], "combined_genera_frequency.log")
    # conda:
    #     "envs/python_scripts.yaml"
    shell:
        """
        python {config[scripts_dir]}/combine_genera_frequency.py {config[results_dir]} {output} 2> {log}
        """