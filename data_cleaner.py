import pandas as pd


def clean_dataset(data):
    cleaned_data = data.copy()

    # Remove completely empty columns
    cleaned_data = cleaned_data.dropna(axis=1, how="all")

    # Remove duplicate rows
    cleaned_data = cleaned_data.drop_duplicates()

    return cleaned_data