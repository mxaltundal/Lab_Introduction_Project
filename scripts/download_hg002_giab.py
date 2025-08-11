#!/usr/bin/env python3
"""Download HG002 GIAB benchmark data files.

This script downloads the HG002 benchmark VCF and BED files from the
Genome in a Bottle (GIAB) FTP site. The default output directory is
``data`` but can be overridden with ``-o`` or ``--outdir``.

Usage::

    python download_hg002_giab.py [--outdir DATA_DIR]

"""
import argparse
import hashlib
import os
from urllib.request import urlretrieve
from urllib.parse import urljoin

BASE_URL = (
    "https://ftp.ncbi.nlm.nih.gov/giab/ftp/release/"
    "AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/"
)
FILES = [
    {
        "name": "HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz",
        "md5": "REPLACE_WITH_MD5",
        "sha256": "REPLACE_WITH_SHA256",
    },
    {
        "name": "HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi",
        "md5": "REPLACE_WITH_MD5",
        "sha256": "REPLACE_WITH_SHA256",
    },
    {
        "name": "HG002_GRCh38_1_22_v4.2.1_benchmark.bed",
        "md5": "REPLACE_WITH_MD5",
        "sha256": "REPLACE_WITH_SHA256",
    },
]

def _compute_checksums(path: str) -> tuple[str, str]:
    """Return the MD5 and SHA256 checksums for ``path``."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def download_file(file_info: dict, outdir: str) -> None:
    """Download a single file from GIAB if it does not already exist."""
    filename = file_info["name"]
    expected_md5 = file_info["md5"]
    expected_sha256 = file_info["sha256"]
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, filename)
    if os.path.exists(dest):
        print(f"[skip] {filename} already exists")
        return
    url = urljoin(BASE_URL, filename)
    print(f"[download] {url} -> {dest}")
    urlretrieve(url, dest)
    md5_sum, sha256_sum = _compute_checksums(dest)
    if md5_sum != expected_md5 or sha256_sum != expected_sha256:
        print(f"[error] Checksum mismatch for {filename}; deleting file")
        os.remove(dest)
    else:
        print(f"[verified] {filename}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Download HG002 GIAB data")
    parser.add_argument(
        "-o",
        "--outdir",
        default="data",
        help="Output directory for downloaded files",
    )
    args = parser.parse_args()

    for info in FILES:
        download_file(info, args.outdir)


if __name__ == "__main__":
    main()
