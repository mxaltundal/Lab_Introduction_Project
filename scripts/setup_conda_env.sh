#!/usr/bin/env bash
# Create and activate the seqc2 conda environment
set -euo pipefail
ENV_FILE="$(dirname "$0")/../environment.yml"

echo "Creating conda environment from $ENV_FILE" >&2
conda env create -f "$ENV_FILE" -n seqc2 || true

echo "Activate the environment with:\n  conda activate seqc2" >&2
