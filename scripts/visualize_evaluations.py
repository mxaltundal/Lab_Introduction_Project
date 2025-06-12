#!/usr/bin/env python3
"""Visualize hap.py evaluation metrics."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot hap.py evaluation metrics")
    parser.add_argument(
        "prefix",
        help="Prefix of hap.py output files (e.g. results/happy)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="evaluation_metrics.png",
        help="Output image file",
    )
    args = parser.parse_args()

    import pandas as pd
    import matplotlib.pyplot as plt

    summary_file = f"{args.prefix}.summary.csv"
    df = pd.read_csv(summary_file)

    metrics = df[df["Type"].isin(["SNP", "INDEL"])]
    plot_df = metrics[["Type", "Recall", "Precision", "F1_Score"]].set_index("Type")
    plot_df.plot(kind="bar")
    plt.ylabel("Score")
    plt.title("hap.py Evaluation Metrics")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Plot saved to {args.output}")


if __name__ == "__main__":
    main()
