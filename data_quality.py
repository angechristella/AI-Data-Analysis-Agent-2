import pandas as pd


def check_data_quality(data):
    quality_report = {}

    # Missing values
    missing = data.isnull().sum()
    quality_report["missing_values"] = {
        column: int(count)
        for column, count in missing.items()
        if count > 0
    }

    # Duplicate rows
    quality_report["duplicate_rows"] = int(data.duplicated().sum())

    # Empty columns
    empty_columns = [
        column for column in data.columns
        if data[column].isnull().all()
    ]
    quality_report["empty_columns"] = empty_columns

    # Negative values in numeric columns
    negative_values = {}

    numeric_columns = data.select_dtypes(include="number").columns

    for column in numeric_columns:
        count = (data[column] < 0).sum()

        if count > 0:
            negative_values[column] = int(count)

    quality_report["negative_values"] = negative_values

    return quality_report