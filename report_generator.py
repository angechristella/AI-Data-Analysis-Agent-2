from html import escape
from datetime import datetime


def generate_html_report(
    original_data,
    cleaned_data,
    insights,
    output_path="analysis_report.html"
):
    original_rows, original_columns = original_data.shape
    cleaned_rows, cleaned_columns = cleaned_data.shape

    missing_values = int(original_data.isnull().sum().sum())
    duplicate_rows = int(original_data.duplicated().sum())

    removed_rows = original_rows - cleaned_rows
    removed_columns = original_columns - cleaned_columns

    # Prepare insights
    insights_html = ""

    for insight in insights:
        insights_html += f"<li>{escape(str(insight))}</li>\n"

    # Prepare column summary
    column_rows = ""

    for column in original_data.columns:
        missing = int(original_data[column].isnull().sum())
        data_type = str(original_data[column].dtype)

        column_rows += (
            "<tr>"
            f"<td>{escape(str(column))}</td>"
            f"<td>{escape(data_type)}</td>"
            f"<td>{missing}</td>"
            "</tr>\n"
        )

    # Build the HTML report
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Data Analysis Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    color: #253047;
    margin: 0;
    line-height: 1.6;
}}
header {{
    background: #17365d;
    color: white;
    padding: 30px;
    text-align: center;
}}
.container {{
    max-width: 1000px;
    margin: 25px auto;
    padding: 20px;
}}
section, .card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px #dddddd;
}}
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 15px;
}}
.metric {{
    font-size: 26px;
    font-weight: bold;
    color: #17365d;
}}
h2 {{
    color: #17365d;
}}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    border: 1px solid #dddddd;
    padding: 10px;
    text-align: left;
    overflow-wrap: anywhere;
}}
th {{
    background: #eaf0f8;
}}
li {{
    margin-bottom: 10px;
}}
button {{
    padding: 12px 18px;
    background: #17365d;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}}
@media print {{
    button {{
        display: none;
    }}
    body {{
        background: white;
    }}
}}
</style>
</head>

<body>
<header>
    <h1>AI Data Analysis Agent</h1>
    <p>Automated Dataset Analysis Report</p>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</header>

<div class="container">

    <button onclick="window.print()">Print or Save as PDF</button>

    <section>
        <h2>1. Executive Summary</h2>
        <p>This report presents the dataset overview, cleaning results,
        data quality, automated insights, and recommendations.</p>
    </section>

    <div class="cards">
        <div class="card">
            <h3>Original Rows</h3>
            <div class="metric">{original_rows:,}</div>
        </div>
        <div class="card">
            <h3>Cleaned Rows</h3>
            <div class="metric">{cleaned_rows:,}</div>
        </div>
        <div class="card">
            <h3>Original Columns</h3>
            <div class="metric">{original_columns:,}</div>
        </div>
        <div class="card">
            <h3>Missing Values</h3>
            <div class="metric">{missing_values:,}</div>
        </div>
        <div class="card">
            <h3>Duplicate Rows</h3>
            <div class="metric">{duplicate_rows:,}</div>
        </div>
    </div>

    <section>
        <h2>2. Cleaning Results</h2>
        <p>Rows removed: <strong>{removed_rows:,}</strong></p>
        <p>Columns removed: <strong>{removed_columns:,}</strong></p>
        <p>These figures compare the original dataset with the cleaned dataset.</p>
    </section>

    <section>
        <h2>3. Column Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Data Type</th>
                    <th>Missing Values</th>
                </tr>
            </thead>
            <tbody>
                {column_rows}
            </tbody>
        </table>
    </section>

    <section>
        <h2>4. Automated Insights and Recommendations</h2>
        <ul>
            {insights_html}
        </ul>
    </section>

    <section>
        <h2>5. Interpretation Notes</h2>
        <ul>
            <li>Review unusual values before treating them as errors.</li>
            <li>Choose a suitable method for handling missing values.</li>
            <li>Correlation does not necessarily mean causation.</li>
            <li>Interpret results in the context of the dataset.</li>
        </ul>
    </section>

</div>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as report_file:
        report_file.write(html_content)

    return output_path

