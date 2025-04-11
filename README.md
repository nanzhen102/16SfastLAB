# 16SfastLAB
 Fast taxonomic classcification of *Lactobacillaceae* from 16S gene sequencing data

### The final result you will get 👉
| | ERR13583988 | ERR13583989|
| Lactobacillus | 0.41|0.22|

### Workflow 🐾
![pdf](./pipeline_dag.pdf)

### Protocol 🧑‍🔧
Step 1. 

Transfer fastq files into `data`folder

Step 2. 

Run `Snakemake`
```bash
snakemake --cores 4
```

Step 3.

Go to the  `results`  folder and check `combined_genera_frequency.csv`.

