import csv, sqlite3, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def analyze():
    with (ROOT/'data/raw_orders.csv').open() as f: raw=list(csv.DictReader(f))
    seen=set(); clean=[]
    for row in raw:
        if row['order_id'] in seen: continue
        seen.add(row['order_id'])
        row['state']=row['state'].strip() or 'Unknown'
        row['quantity']=int(row['quantity'])
        for k in ['unit_price','unit_cost','discount','revenue','profit']: row[k]=float(row[k])
        clean.append(row)
    with (ROOT/'data/clean_orders.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=clean[0]); w.writeheader(); w.writerows(clean)
    con=sqlite3.connect(ROOT/'data/ecommerce.db')
    con.execute('DROP TABLE IF EXISTS orders')
    con.execute('CREATE TABLE orders (order_id TEXT PRIMARY KEY, order_date TEXT, customer_id TEXT, product TEXT, category TEXT, state TEXT, quantity INTEGER, unit_price REAL, unit_cost REAL, discount REAL, revenue REAL, profit REAL)')
    con.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',[tuple(r.values()) for r in clean]); con.commit()
    revenue=sum(r['revenue'] for r in clean); profit=sum(r['profit'] for r in clean)
    counts={}
    for r in clean: counts[r['customer_id']]=counts.get(r['customer_id'],0)+1
    summary=dict(raw_rows=len(raw),orders=len(clean),duplicates_removed=len(raw)-len(clean),unknown_states=sum(r['state']=='Unknown' for r in clean),revenue=round(revenue,2),profit=round(profit,2),aov=round(revenue/len(clean),2),margin_pct=round(100*profit/revenue,2),customers=len(counts),repeat_customer_pct=round(100*sum(v>1 for v in counts.values())/len(counts),2))
    (ROOT/'reports/summary.json').write_text(json.dumps(summary,indent=2))
    queries={'monthly_sales':"SELECT substr(order_date,1,7) month, sum(revenue) revenue, sum(profit) profit FROM orders GROUP BY month ORDER BY month",'category_performance':"SELECT category, sum(revenue) revenue, sum(profit) profit FROM orders GROUP BY category ORDER BY revenue DESC",'state_performance':"SELECT state, sum(revenue) revenue, sum(profit) profit FROM orders GROUP BY state ORDER BY revenue DESC"}
    for name,q in queries.items():
        cur=con.execute(q)
        with (ROOT/f'reports/{name}.csv').open('w',newline='') as f:
            w=csv.writer(f); w.writerow([d[0] for d in cur.description]); w.writerows(cur)
    top=con.execute(queries['category_performance']).fetchone()
    (ROOT/'reports/business_insights.md').write_text(f"# Findings from synthetic data\n\nRevenue: INR {revenue:,.2f}; profit: INR {profit:,.2f}; margin: {summary['margin_pct']}%.\n\n{top[0]} leads revenue with INR {top[1]:,.2f}. Compare margin before prioritizing inventory.\n\n{summary['unknown_states']} orders have unknown states: fix address capture before geographic decisions.\n\nRepeat customers are customers with more than one order across the complete two-year dataset. This is not a retention or cohort rate.\n\nThese generated observations demonstrate analysis only; they are not evidence about a real business.")
    con.close(); print(json.dumps(summary,indent=2))
if __name__=='__main__': analyze()
