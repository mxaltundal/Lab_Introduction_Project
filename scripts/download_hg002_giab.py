#!/usr/bin/env python3
"""Download HG002 GIAB benchmark data files.

This script downloads the HG002 benchmark VCF and BED files from the
Genome in a Bottle (GIAB) FTP site. The default output directory is
``data`` but can be overridden with ``-o`` or ``--outdir``.

Usage::

    python download_hg002_giab.py [--outdir DATA_DIR]

"""
import argparse
import os
from urllib.request import urlretrieve
from urllib.parse import urljoin

BASE_URL = (
    "https://ftp.ncbi.nlm.nih.gov/giab/ftp/release/"
    "AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/"
)
FILES = [
    "HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz",
    "HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi",
    "HG002_GRCh38_1_22_v4.2.1_benchmark.bed",
]

def download_file(filename: str, outdir: str) -> None:
    """Download a single file from GIAB if it does not already exist."""
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, filename)
    if os.path.exists(dest):
        print(f"[skip] {filename} already exists")
        return
    url = urljoin(BASE_URL, filename)
    print(f"[download] {url} -> {dest}")
    urlretrieve(url, dest)

def main() -> None:
    parser = argparse.ArgumentParser(description="Download HG002 GIAB data")
    parser.add_argument(
        "-o",
        "--outdir",
        default="data",
        help="Output directory for downloaded files",
    )
    args = parser.parse_args()

    for fname in FILES:
        download_file(fname, args.outdir)


if __name__ == "__main__":
    main()
