import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def create_visualizations(data):
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    chart_count = 0

    # Select numeric columns
    numeric_columns = data.select_dtypes(
        include="number"
    ).columns

    # Create histograms
    for column in numeric_columns[:5]:
        values = data[column].dropna()

        if values.empty or values.nunique() < 2:
            continue

        plt.figure(figsize=(8, 5))
        plt.hist(values, bins=20)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()

        filename = os.path.join(
            output_folder,
            f"{column}_distribution.png"
        )

        plt.savefig(filename)
        plt.close()

        chart_count += 1

    # Create a missing-values chart
    missing = data.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        plt.figure(figsize=(10, 5))
        missing.sort_values().plot(kind="bar")

        plt.title("Missing Values by Column")
        plt.xlabel("Column")
        plt.ylabel("Number of Missing Values")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        filename = os.path.join(
            output_folder,
            "missing_values.png"
        )

        plt.savefig(filename)
        plt.close()

        chart_count += 1

    return chart_count