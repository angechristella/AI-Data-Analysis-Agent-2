import pandas as pd

def answer_question(data, question):
    question = question.lower().strip()


    if "how many rows" in question:
        return f"The dataset contains {len(data)} rows."

    if "how many columns" in question:
        return f"The dataset contains {len(data.columns)} columns."

    if "column names" in question or "what are the columns" in question:
        return "Columns: " + ", ".join(data.columns.astype(str))

    if "missing values" in question:
        missing = data.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
           return "There are no missing values."

        return missing.to_string()

    if "duplicate" in question:
        return f"Duplicate rows: {data.duplicated().sum()}"

    numeric_columns = data.select_dtypes(include="number").columns

    if "average" in question or "mean" in question:
        for column in numeric_columns:
            if str(column).lower() in question:
               value = data[column].mean()

               if pd.isna(value):
                   return f"No usable numeric values in {column}."

               return f"Average {column}: {value:.2f}"

        return "Include a numeric column name, such as 'What is the average price?'"

    if "highest" in question or "maximum" in question:
        for column in numeric_columns:
            if str(column).lower() in question:
                return f"Highest {column}: {data[column].max()}"

        return "Include a numeric column name."

    if "lowest" in question or "minimum" in question:
         for column in numeric_columns:
             if str(column).lower() in question:
                 return f"Lowest {column}: {data[column].min()}"

    return "Include a numeric column name."

    if "most common" in question or "most frequent" in question:
        for column in data.columns:
            if str(column).lower() in question:
                values = data[column].dropna()

                if values.empty:
                    return f"No available values in {column}."

            return f"Most common {column}: {values.mode().iloc[0]}"

        return "Include a column name."

    if "summary statistics" in question or "describe the data" in question:
        if len(numeric_columns) == 0:
            return "There are no numeric columns to summarize."

        return data[numeric_columns].describe().round(2).to_string()

    return (
    "I cannot answer that question yet. Try asking about rows, columns, "
    "missing values, duplicates, average, highest, lowest, "
    "most common values, or summary statistics."
)

