import pandas as pd

from data_analyzer import inspect_dataset
from data_quality import check_data_quality
from data_cleaner import clean_dataset
from insight_generator import generate_insights
from visualizer import create_visualizations
from question_answer import answer_question
from report_generator import generate_html_report

def main():
    print("AI Data Analysis Agent")
    print("======================")

    file_path = input("Enter the path to your CSV file: ")

    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        print("\nDataset loaded successfully!")

        # -----------------------------
        # DATASET INSPECTION
        # -----------------------------

        results = inspect_dataset(data)

        print("\n--- DATASET OVERVIEW ---")
        print(f"Rows: {results['rows']}")
        print(f"Columns: {results['columns']}")

        print("\n--- COLUMNS ---")
        for column in results["column_names"]:
            print(f"- {column}")

        print("\n--- DATA TYPES ---")
        for column, data_type in results["data_types"].items():
            print(f"{column}: {data_type}")

        # -----------------------------
        # DATA QUALITY
        # -----------------------------

        quality = check_data_quality(data)

        print("\n--- DATA QUALITY REPORT ---")

        print("\nMissing values:")
        if quality["missing_values"]:
            for column, count in quality["missing_values"].items():
                print(f"- {column}: {count}")
        else:
            print("No missing values found.")

        print(f"\nDuplicate rows: {quality['duplicate_rows']}")

        print("\nEmpty columns:")
        if quality["empty_columns"]:
            for column in quality["empty_columns"]:
                print(f"- {column}")
        else:
            print("No completely empty columns found.")

        print("\nNegative values:")
        if quality["negative_values"]:
            for column, count in quality["negative_values"].items():
                print(f"- {column}: {count}")
        else:
            print("No negative values found.")

        # -----------------------------
        # DATA CLEANING
        # -----------------------------

        cleaned_data = clean_dataset(data)

        cleaned_data.to_csv("cleaned_dataset.csv", index=False)

        print("\n--- CLEANING RESULTS ---")
        print(f"Original rows: {data.shape[0]}")
        print(f"Cleaned rows: {cleaned_data.shape[0]}")
        print(f"Original columns: {data.shape[1]}")
        print(f"Cleaned columns: {cleaned_data.shape[1]}")

        # -----------------------------
        # AUTOMATIC INSIGHTS
        # -----------------------------

        insights = generate_insights(cleaned_data)

        print("\n--- AUTOMATIC DATA INSIGHTS ---")

        for number, insight in enumerate(insights, start=1):
            print(f"{number}. {insight}")

        # Save the insights report
        with open(
            "insights_report.txt", "w", encoding="utf-8"
        ) as file:
            file.write("AI DATA ANALYSIS AGENT - INSIGHTS REPORT\n\n")

            for number, insight in enumerate(insights, start=1):
                file.write(f"{number}. {insight}\n")

        print("\nInsights report saved as insights_report.txt")

        # -----------------------------
        # GENERATE HTML REPORT
        # -----------------------------

        report_path = generate_html_report(
            original_data=data,
            cleaned_data=cleaned_data,
            insights=insights,
            output_path="analysis_report.html"
        )

        print(f"\nHTML report saved as {report_path}")

        # -----------------------------
        # NUMERICAL SUMMARY
        # -----------------------------

        print("\n--- NUMERICAL SUMMARY ---")
        print(data.describe())

        # -----------------------------
        # ASK QUESTIONS ABOUT THE DATA
        # -----------------------------
        print("\n--- ASK QUESTIONS ABOUT YOUR DATA ---")
        print("Type 'exit' to stop asking questions.")

        while True:
            question = input("\nYour question: ").strip()

            if question.lower() == "exit":
                print("Question session ended.")
                break

            if not question:
                print("Please enter a question.")
                continue

            answer = answer_question(cleaned_data, question)
            print("\nAnswer:")
            print(answer)
        # -----------------------------
        # AUTOMATIC VISUALIZATIONS
        # -----------------------------

        chart_count = create_visualizations(cleaned_data)

        print("\n--- VISUALIZATION RESULTS ---")
        print(f"Charts created: {chart_count}")
        print("Charts saved in the outputs folder.")

    except FileNotFoundError:
        print("\nError: The CSV file was not found.")
        print("Check the filename and try again.")

    except pd.errors.EmptyDataError:
        print("\nError: The CSV file is empty.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
