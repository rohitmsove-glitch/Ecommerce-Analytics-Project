# Data dictionary and portfolio notes
| Column | Meaning |
|---|---|
| order_id | Unique complete order identifier |
| order_date | Purchase date, 2024–2025 |
| customer_id | Synthetic customer identifier |
| product, category | Product and its grouping |
| state | Synthetic delivery state; missing values become Unknown |
| quantity | Units in order |
| unit_price, unit_cost | INR selling price before discount and product cost |
| discount | Fraction between 0 and 0.2 |
| revenue | quantity × unit_price × (1 − discount) |
| profit | revenue − quantity × unit_cost |

## KPI definitions
AOV = total revenue / unique orders. Margin = total profit / revenue. Repeat customer rate = customers with more than one order / all customers, within the analysis period. YoY compares like calendar periods and requires prior-year data. RFM uses 2026-01-01 as its snapshot date; recency is days since the last order.

## Resume description (after you run and understand the project)
**E-Commerce Sales & Customer Analytics | Python, SQL, Streamlit; Power BI after completing the build guide**
- Analyzed 5,000 synthetic orders using a reproducible Python and SQLite pipeline.
- Removed 25 duplicate records and labeled 20 missing delivery states for transparent geographic analysis.
- Built a dashboard with revenue, profit, AOV, margin, sales trends, product analysis and customer purchase frequency.
- Wrote SQL for category performance, year-over-year growth and RFM customer analysis.
Only list Power BI after building the PBIX yourself. Do not claim actual company revenue improvements.

## Explain in an interview
Discuss the unique-order key, how duplicate rows distort KPIs, why Unknown is preferable to guessing states, and why product gross profit differs from business net profit. Explain the effect of date filters on repeat customer rate. Extend with a real licensed dataset, returns, cohort retention and multi-line orders before claiming production realism.
