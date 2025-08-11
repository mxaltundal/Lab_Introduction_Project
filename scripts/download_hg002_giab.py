#!/usr/bin/env python3
"""Download HG002 GIAB benchmark data files.

This script downloads the HG002 benchmark VCF and BED files from the
Genome in a Bottle (GIAB) FTP site. The default output directory is
``data`` but can be overridden with ``-o`` or ``--outdir``.

Usage::

    python download_hg002_giab.py [--outdir DATA_DIR]

"""
import argparse
import logging
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
        logging.info("[skip] %s already exists", filename)
        return
    url = urljoin(BASE_URL, filename)
    logging.info("[download] %s -> %s", url, dest)
    urlretrieve(url, dest)

def main() -> None:
    parser = argparse.ArgumentParser(description="Download HG002 GIAB data")
    parser.add_argument(
        "-o",
        "--outdir",
        default="data",
        help="Output directory for downloaded files",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(levelname)s: %(message)s",
    )

    for fname in FILES:
        download_file(fname, args.outdir)


if __name__ == "__main__":
    main()
