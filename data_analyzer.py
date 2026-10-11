import pandas as pd


def inspect_dataset(data):
    results = {}

    results["rows"] = data.shape[0]
    results["columns"] = data.shape[1]
    results["column_names"] = list(data.columns)

    results["data_types"] = data.dtypes.astype(str).to_dict()

    results["missing_values"] = data.isnull().sum().to_dict()

    results["duplicate_rows"] = int(data.duplicated().sum())

    results["numeric_summary"] = data.describe().to_dict()

    return results