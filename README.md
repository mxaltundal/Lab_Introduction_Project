# Lab_Introduction_Project

# SEQC2 GIAB Variant Calling Evaluation

This project aims to reproduce and evaluate variant calling pipelines using the SEQC2-recommended reference sample HG002 from the Genome in a Bottle (GIAB) consortium.

## Steps:
1. Download HG002 GIAB data
2. Set up Python conda environment
3. Install variant calling tools (DeepVariant)
4. Run evaluation pipeline

## Environment:
- Python 3.10
- Conda environment: `seqc2`
- Tools: DeepVariant

## Data Sources:
- GIAB: [ftp://ftp-trace.ncbi.nlm.nih.gov/giab/](ftp://ftp-trace.ncbi.nlm.nih.gov/giab/)

### Downloading HG002 data

Use the `download_hg002_giab.py` script to fetch the benchmark VCF and BED files:

```bash
python scripts/download_hg002_giab.py --outdir data
```

This will create a `data` directory containing the HG002 benchmark files required for evaluation.

### Setting up the conda environment

Create the Python environment and install the required tools using `environment.yml`:

```bash
conda env create -f environment.yml
conda activate seqc2
```

The environment installs **DeepVariant** from Bioconda.

### Running the evaluation pipeline

After downloading the HG002 truth data and creating the environment,
run the pipeline to generate variant calls with DeepVariant and compare
them to the GIAB benchmark set using `hap.py`:

```bash
python scripts/run_evaluation_pipeline.py \
  --bam path/to/aligned.bam \
  --ref path/to/reference.fasta \
  --outdir results
```

This will produce a `results` directory containing the DeepVariant VCF and
evaluation metrics from `hap.py`.
### Visualizing hap.py evaluation results

After running the evaluation pipeline, you can plot the `hap.py` metrics using:

```bash
python scripts/visualize_evaluations.py results/happy -o evaluation_metrics.png
```

This creates an `evaluation_metrics.png` bar chart summarizing SNP and INDEL recall, precision, and F1 score.

Alternatively, run the helper script:

```bash
./scripts/setup_conda_env.sh
```
