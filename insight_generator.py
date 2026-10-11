import pandas as pd


def generate_insights(data):
    insights = []

    if data.empty:
        return ["The dataset is empty. No insights can be generated."]

    rows, columns = data.shape

    # 1. Dataset overview
    insights.append("=== DATASET OVERVIEW ===")
    insights.append(
        f"The dataset contains {rows:,} rows and {columns} columns."
    )

    # 2. Missing values
    insights.append("\n=== MISSING VALUES ===")

    missing = data.isnull().sum()
    total_missing = int(missing.sum())

    if total_missing > 0:
        insights.append(
            f"Total missing values: {total_missing:,}"
        )

        for column, count in missing.items():
            if count > 0:
                percentage = (count / rows) * 100

                insights.append(
                    f"{column}: {count:,} missing values "
                    f"({percentage:.2f}% of rows)."
                )

                if percentage >= 30:
                    insights.append(
                        f"Recommendation: Review {column}, "
                        "because at least 30% of its values are missing."
                    )
    else:
        insights.append("The dataset has no missing values.")

    # 3. Duplicate rows
    insights.append("\n=== DUPLICATE ROWS ===")

    duplicates = int(data.duplicated().sum())

    insights.append(
        f"The dataset contains {duplicates:,} duplicate rows."
    )

    if duplicates > 0:
        insights.append(
            "Recommendation: Review duplicate rows before analysis."
        )

    # 4. Numeric column analysis
    insights.append("\n=== NUMERIC ANALYSIS ===")

    numeric_data = data.select_dtypes(include="number")

    if numeric_data.empty:
        insights.append("No numeric columns were found.")
    else:
        for column in numeric_data.columns:
            values = numeric_data[column].dropna()

            if values.empty:
                insights.append(
                    f"{column}: no usable numeric values."
                )
                continue

            average = values.mean()
            median = values.median()
            minimum = values.min()
            maximum = values.max()
            standard_deviation = values.std()

            insights.append(
                f"{column}: mean = {average:.2f}, "
                f"median = {median:.2f}, "
                f"minimum = {minimum:.2f}, "
                f"maximum = {maximum:.2f}, "
                f"standard deviation = {standard_deviation:.2f}."
            )

            # Identify possible extreme values using the IQR method
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            if iqr > 0:
                lower_limit = q1 - 1.5 * iqr
                upper_limit = q3 + 1.5 * iqr

                unusual_count = int(
                    ((values < lower_limit) |
                     (values > upper_limit)).sum()
                )

                if unusual_count > 0:
                    insights.append(
                        f"{column}: {unusual_count:,} values fall "
                        "outside the usual IQR range. Review them "
                        "before deciding whether they are errors."
                    )

    # 5. Negative values
    insights.append("\n=== NEGATIVE VALUES ===")

    negative_columns = []

    for column in numeric_data.columns:
        negative_count = int((numeric_data[column] < 0).sum())

        if negative_count > 0:
            negative_columns.append(
                f"{column}: {negative_count:,} negative values"
            )

    if negative_columns:
        insights.extend(negative_columns)
        insights.append(
            "Recommendation: Check whether negative values are valid "
            "for these columns before changing them."
        )
    else:
        insights.append(
            "No negative values were found in numeric columns."
        )

    # 6. Most common categories
    insights.append("\n=== COMMON CATEGORIES ===")

    categorical_data = data.select_dtypes(
        include=["object", "category", "string"]
    )

    if categorical_data.empty:
        insights.append("No text or category columns were found.")
    else:
        for column in categorical_data.columns:
            values = data[column].dropna()

            if values.empty:
                continue

            if values.nunique() <= 50:
                common_value = values.mode()

                if not common_value.empty:
                    frequency = int(
                        (values == common_value.iloc[0]).sum()
                    )

                    insights.append(
                        f"{column}: most common value is "
                        f"'{common_value.iloc[0]}', appearing "
                        f"{frequency:,} times."
                    )

    # 7. Correlations between numeric columns
    insights.append("\n=== NUMERIC RELATIONSHIPS ===")

    if len(numeric_data.columns) >= 2:
        correlations = numeric_data.corr()

        found_relationship = False

        for i in range(len(correlations.columns)):
            for j in range(i + 1, len(correlations.columns)):
                column_a = correlations.columns[i]
                column_b = correlations.columns[j]
                correlation = correlations.iloc[i, j]

                if pd.isna(correlation):
                    continue

                if abs(correlation) >= 0.7:
                    direction = (
                        "positive"
                        if correlation > 0
                        else "negative"
                    )

                    insights.append(
                        f"{column_a} and {column_b} have a strong "
                        f"{direction} correlation "
                        f"({correlation:.2f}). This indicates an "
                        "association, not necessarily causation."
                    )

                    found_relationship = True

        if not found_relationship:
            insights.append(
                "No strong numeric correlations were identified "
                "using the 0.70 threshold."
            )
    else:
        insights.append(
            "At least two numeric columns are needed to examine "
            "correlations."
        )

    # 8. Final recommendation
    insights.append("\n=== GENERAL RECOMMENDATIONS ===")

    if total_missing > 0:
        insights.append(
            "Review missing values and decide how to handle them "
            "before drawing conclusions."
        )

    if duplicates > 0:
        insights.append(
            "Check duplicate records to determine whether they "
            "should be retained or removed."
        )

    insights.append(
        "Check unusual values and confirm that column data types "
        "are appropriate for the analysis."
    )

    insights.append(
        "Interpret findings using the meaning of each column "
        "and the context of the dataset."
    )

    return insights

