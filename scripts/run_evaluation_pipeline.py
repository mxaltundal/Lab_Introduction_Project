#!/usr/bin/env python3
"""Run variant calling and evaluate results against HG002 benchmarks.

This script executes DeepVariant or GATK to call variants from an aligned
BAM/CRAM file and then compares the calls against the Genome in a Bottle HG002
truth set using ``hap.py``.

Example::

    python scripts/run_evaluation_pipeline.py \
        --bam sample.bam \
        --ref GRCh38.fa \
        --outdir results \
        --caller gatk
"""
import argparse
import os
import subprocess
from typing import List

def run(cmd: List[str]) -> None:
    """Run a command and stream output."""
    print("[run]", " ".join(cmd))
    subprocess.run(cmd, check=True)

def run_deepvariant(bam: str, ref: str, out_dir: str) -> str:
    """Run DeepVariant and return the path to the output VCF."""
    vcf_path = os.path.join(out_dir, "deepvariant.vcf.gz")
    cmd = [
        "run_deepvariant",
        f"--model_type=WGS",
        f"--ref={ref}",
        f"--reads={bam}",
        f"--output_vcf={vcf_path}",
        f"--num_shards={os.cpu_count() or 1}",
    ]
    run(cmd)
    return vcf_path


def run_gatk(bam: str, ref: str, out_dir: str) -> str:
    """Run GATK HaplotypeCaller and return the path to the output VCF."""
    vcf_path = os.path.join(out_dir, "gatk.vcf.gz")
    cmd = [
        "gatk",
        "HaplotypeCaller",
        "-R",
        ref,
        "-I",
        bam,
        "-O",
        vcf_path,
    ]
    run(cmd)
    return vcf_path

def run_happy(truth_vcf: str, truth_bed: str, query_vcf: str, ref: str, out_dir: str) -> None:
    """Compare query VCF against truth using hap.py."""
    cmd = [
        "hap.py",
        truth_vcf,
        query_vcf,
        "-f",
        truth_bed,
        "-r",
        ref,
        "-o",
        os.path.join(out_dir, "happy"),
    ]
    run(cmd)

def main() -> None:
    parser = argparse.ArgumentParser(description="Run variant calling and evaluation")
    parser.add_argument("--bam", required=True, help="Input aligned BAM/CRAM file")
    parser.add_argument("--ref", required=True, help="Reference FASTA")
    parser.add_argument("--truth-vcf", default="data/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz", help="Benchmark VCF")
    parser.add_argument("--truth-bed", default="data/HG002_GRCh38_1_22_v4.2.1_benchmark.bed", help="Benchmark BED")
    parser.add_argument("-o", "--outdir", default="results", help="Output directory")
    parser.add_argument(
        "--caller",
        choices=["deepvariant", "gatk"],
        default="deepvariant",
        help="Variant caller to use",
    )
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    if args.caller == "deepvariant":
        query_vcf = run_deepvariant(args.bam, args.ref, args.outdir)
    else:
        query_vcf = run_gatk(args.bam, args.ref, args.outdir)
    run_happy(args.truth_vcf, args.truth_bed, query_vcf, args.ref, args.outdir)

if __name__ == "__main__":
    main()
