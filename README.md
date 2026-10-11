# E-Commerce Sales & Customer Analytics
A complete runnable educational portfolio project with synthetic Indian e-commerce data, cleaning, SQLite analysis, exported findings, a Streamlit dashboard and Power BI build assets.

## Quick start on Windows / VS Code
1. Extract this ZIP and open the ecommerce-analytics folder in VS Code.
2. Install Python 3.10 or newer if needed; open a terminal in this folder.
3. Run `python -m venv .venv`, then `.venv\Scripts\activate`.
4. Run `python -m pip install -r requirements.txt`.
5. Run `python -m streamlit run app.py`. Open the localhost URL displayed.
On macOS/Linux activate with `source .venv/bin/activate`. Installing packages requires internet access.

## Reproduce the analysis
The cleaned CSV, SQLite database and reports are already included. Rebuild with:
```
python generate_data.py
python analyze.py
python verify.py
```
These commands use only the Python standard library. They overwrite generated data/reports. The random seed is fixed at 42.
Run sql/analysis.sql using DB Browser for SQLite or a SQLite editor against data/ecommerce.db. See powerbi/SETUP.md for Power BI Desktop instructions.

## Contents
- generate_data.py: reproducible dataset, 5,000 unique orders and 25 deliberate duplicate rows.
- analyze.py: deduplication, unknown-state labeling, numeric conversions, SQLite load, KPI and grouped report exports.
- app.py: date/category/state filters, five KPIs, sales trend, category/state/product analysis, repeat-customer metric and filtered CSV download.
- sql/: business queries, year-over-year comparison and RFM inputs.
- powerbi/: DAX measures and dashboard build guide (no native PBIX included).
- reports/: generated metrics, CSV summaries and business findings.
- docs.md: data dictionary, assumptions and resume/interview notes.

## Scope
All records are generated, not sourced from a company. Revenue is after discount; profit is revenue minus product cost and excludes shipping, tax, returns and overhead. One row equals one order containing one product type. There is no causal evidence of business improvement. Dashboard dependencies must be installed locally.
