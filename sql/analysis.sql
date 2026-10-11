-- SQLite queries: run against data/ecommerce.db.
SELECT SUM(revenue) revenue, SUM(profit) profit, COUNT(*) orders,
       SUM(revenue)/COUNT(*) aov, 100.0*SUM(profit)/SUM(revenue) margin_pct FROM orders;
SELECT category, SUM(revenue) revenue, SUM(profit) profit,
       100.0*SUM(profit)/SUM(revenue) margin_pct FROM orders GROUP BY category;
SELECT product, SUM(revenue) revenue FROM orders GROUP BY product ORDER BY revenue DESC LIMIT 10;
SELECT state, SUM(revenue) revenue FROM orders GROUP BY state ORDER BY revenue DESC;
SELECT substr(order_date,1,7) month, SUM(revenue) revenue FROM orders GROUP BY month ORDER BY month;
WITH annual AS (SELECT substr(order_date,1,4) year, SUM(revenue) revenue FROM orders GROUP BY year)
SELECT year,revenue,100.0*(revenue/LAG(revenue) OVER (ORDER BY year)-1) yoy_pct FROM annual;
WITH frequency AS (SELECT customer_id,COUNT(*) n FROM orders GROUP BY customer_id)
SELECT COUNT(*) customers,SUM(CASE WHEN n>1 THEN 1 ELSE 0 END) repeat_customers FROM frequency;
-- RFM at fixed snapshot 2026-01-01; monetary uses revenue, not profit.
SELECT customer_id, CAST(julianday('2026-01-01')-julianday(MAX(order_date)) AS INTEGER) recency_days,
       COUNT(*) frequency, SUM(revenue) monetary FROM orders GROUP BY customer_id;
