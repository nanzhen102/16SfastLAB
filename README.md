# 16SfastLAB
 fast taxonomic classcification of Lactobacillaceae from 16S gene sequencing data

#### The final result you will get 👉
| | 

#### Workflow 🧑
![pdf](./pipeline_dag.pdf)

## Protocol 🧑‍🔧
Step 1. Transfer fastq files into `data`folder

Step 2. 
```bash
snakemake --cores 4
```

Step 3.
Go to the  `results`  folder and check `combined_genera_frequency.csv`.

