import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import tempfile

from data_analyzer import inspect_dataset
from data_quality import check_data_quality
from data_cleaner import clean_dataset
from insight_generator import generate_insights
from visualizer import create_visualizations
from question_answer import answer_question
from report_generator import generate_html_report


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Data Analysis Agent",
    page_icon="",
    layout="wide"
)


# -----------------------------
# PAGE HEADER
# -----------------------------

st.title(" AI Data Analysis Agent")

st.write(
    "Upload a CSV dataset to inspect, clean, analyze, "
    "visualize, and explore your data."
)

st.info(
    "Your analysis runs locally on your computer. "
    "The application uses your existing Python analysis modules."
)


# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)


if uploaded_file is not None:

    try:
        # Load dataset
        data = pd.read_csv(uploaded_file)

        if data.empty:
            st.warning("The uploaded dataset contains no data.")
            st.stop()

        st.success("Dataset uploaded successfully!")

        # -----------------------------
        # DATASET OVERVIEW
        # -----------------------------

        st.header("1. Dataset Overview")

        results = inspect_dataset(data)

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", f"{results['rows']:,}")
        col2.metric("Columns", f"{results['columns']:,}")
        col3.metric(
            "Duplicate Rows",
            f"{int(data.duplicated().sum()):,}"
        )

        with st.expander("Preview Dataset"):
            st.dataframe(data.head(100), use_container_width=True)

        with st.expander("Column Names and Data Types"):
            column_info = pd.DataFrame({
                "Column": data.columns.astype(str),
                "Data Type": data.dtypes.astype(str).values,
                "Missing Values": data.isnull().sum().values
            })

            st.dataframe(column_info, use_container_width=True)

        # -----------------------------
        # DATA QUALITY
        # -----------------------------

        st.header("2. Data Quality")

        quality = check_data_quality(data)

        quality_col1, quality_col2 = st.columns(2)

        quality_col1.metric(
            "Missing Values",
            f"{int(data.isnull().sum().sum()):,}"
        )

        quality_col2.metric(
            "Duplicate Rows",
            f"{int(data.duplicated().sum()):,}"
        )

        with st.expander("View Data Quality Details"):
            st.subheader("Missing Values")

            missing = data.isnull().sum()
            missing = missing[missing > 0]

            if missing.empty:
                st.write("No missing values found.")
            else:
                st.dataframe(
                    missing.rename("Missing Count").to_frame()
                )

            st.subheader("Completely Empty Columns")

            if quality["empty_columns"]:
                st.write(quality["empty_columns"])
            else:
                st.write("No completely empty columns found.")

            st.subheader("Negative Values")

            if quality["negative_values"]:
                st.write(quality["negative_values"])
            else:
                st.write("No negative values found in numeric columns.")

        # -----------------------------
        # DATA CLEANING
        # -----------------------------

        st.header("3. Data Cleaning")

        cleaned_data = clean_dataset(data)

        clean_col1, clean_col2, clean_col3 = st.columns(3)

        clean_col1.metric(
            "Original Rows",
            f"{len(data):,}"
        )

        clean_col2.metric(
            "Cleaned Rows",
            f"{len(cleaned_data):,}"
        )

        clean_col3.metric(
            "Rows Removed",
            f"{len(data) - len(cleaned_data):,}"
        )

        st.write(
            "The current cleaning function removes duplicate rows "
            "and completely empty columns. It does not automatically "
            "fill missing values."
        )

        csv_buffer = BytesIO()

        cleaned_data.to_csv(
            csv_buffer,
            index=False,
            encoding="utf-8"
        )

        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv_buffer.getvalue(),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

        # -----------------------------
        # AUTOMATIC INSIGHTS
        # -----------------------------

        st.header("4. Automatic Insights")

        insights = generate_insights(cleaned_data)

        for insight in insights:
            st.write(f"• {insight}")

        insights_text = (
            "AI DATA ANALYSIS AGENT - INSIGHTS REPORT\n\n"
            + "\n".join(
                f"{number}. {insight}"
                for number, insight in enumerate(insights, start=1)
            )
        )

        st.download_button(
            label="⬇️ Download Insights Report",
            data=insights_text,
            file_name="insights_report.txt",
            mime="text/plain"
        )

        # -----------------------------
        # NUMERICAL SUMMARY
        # -----------------------------

        st.header("5. Numerical Summary")

        numeric_data = cleaned_data.select_dtypes(include="number")

        if numeric_data.empty:
            st.write("No numeric columns are available.")
        else:
            st.dataframe(
                numeric_data.describe().round(2),
                use_container_width=True
            )

        # -----------------------------
        # ASK QUESTIONS
        # -----------------------------

        st.header("6. Ask Questions About Your Data")

        st.write(
            "Try asking about rows, columns, missing values, "
            "duplicates, averages, highest values, or lowest values."
        )

        with st.form("question_form"):
            question = st.text_input(
                "Enter your question",
                placeholder="What is the average price?"
            )

            ask_button = st.form_submit_button("Ask Question")

        if ask_button:
            if question.strip():
                answer = answer_question(
                    cleaned_data,
                    question
                )

                st.subheader("Answer")
                st.write(answer)
            else:
                st.warning("Please enter a question.")

        # -----------------------------
        # VISUALIZATIONS
        # -----------------------------

        st.header("7. Data Visualizations")

        if st.button("Generate Visualizations"):
            with st.spinner("Generating charts..."):
                chart_count = create_visualizations(cleaned_data)

            st.success(
                f"Generated {chart_count} chart(s)."
            )

            output_folder = Path("outputs")

            if output_folder.exists():
                chart_files = sorted(
                    list(output_folder.glob("*.png"))
                    + list(output_folder.glob("*.jpg"))
                    + list(output_folder.glob("*.jpeg"))
                )

                if chart_files:
                    for chart_path in chart_files:
                        st.subheader(chart_path.stem.replace("_", " ").title())
                        st.image(
                            str(chart_path),
                            use_container_width=True
                        )
                else:
                    st.info(
                        "No PNG or JPG charts were found in the outputs folder."
                    )
            else:
                st.info(
                    "The outputs folder was not found."
                )

        # -----------------------------
        # HTML REPORT
        # -----------------------------

        st.header("8. Professional HTML Report")

        if st.button("Generate HTML Report"):

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".html",
                encoding="utf-8",
                delete=False
            ) as temp_file:
                report_path = temp_file.name

            try:
                generate_html_report(
                    original_data=data,
                    cleaned_data=cleaned_data,
                    insights=insights,
                    output_path=report_path
                )

                with open(
                    report_path,
                    "rb"
                ) as report_file:
                    report_bytes = report_file.read()

                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=report_bytes,
                    file_name="analysis_report.html",
                    mime="text/html"
                )

                st.success("HTML report generated successfully!")

            finally:
                Path(report_path).unlink(missing_ok=True)

        st.success(
            "Analysis complete! Explore the sections above "
            "or download your results."
        )

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")

    except Exception as error:
        st.error(
            f"An error occurred during analysis: {error}"
        )

else:
    st.info(
        "Upload a CSV file above to begin your analysis."
    )

    st.subheader("Available Features")

    st.markdown(
        """
        -  Upload CSV datasets
        -  Inspect rows, columns, and data types
        -  Clean duplicate rows and empty columns
        -  Review data quality
        -  Generate automatic insights
        -  View numerical summaries
        -  Ask questions about your data
        -  Generate visualizations
        -  Download reports and cleaned data
        """
    )