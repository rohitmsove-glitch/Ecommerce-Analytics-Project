# Build the Power BI dashboard
A .pbix file is not included. Create it in Power BI Desktop using these assets.
1. Get Data > Text/CSV > select data/clean_orders.csv > Transform Data.
2. Rename the query Orders. Set order_date to Date, quantity to Whole Number, and price/cost/discount/revenue/profit to Decimal Number. Load.
3. Create a calculated table: Calendar = CALENDAR(DATE(2024,1,1),DATE(2025,12,31)).
4. Mark Calendar as a date table using Date. Create an active one-to-many relationship Calendar[Date] to Orders[order_date], with single-direction filtering.
5. Create each measure in measures.dax separately. Format monetary measures as INR currency and margin/YoY/repeat rate as percentages.
6. Add KPI cards for revenue, profit, orders, AOV and margin. Add a line chart using Calendar[Date] by month and Total Revenue. Add category/state/product bar charts and date/category/state slicers.
7. Add a second page with customer count, repeat rate and customer-level order count/revenue table.
8. Validate unfiltered KPIs against reports/summary.json. Save as EcommerceAnalytics.pbix.
YoY returns blank when prior-year data is absent. Repeat rate is measured in the current filter context. Each row is a complete single-product order; do not treat it as a multi-line transaction table.
