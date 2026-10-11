import csv,json,sqlite3,math
from pathlib import Path
r=Path(__file__).resolve().parent
s=json.loads((r/'reports/summary.json').read_text())
with (r/'data/clean_orders.csv').open() as f: rows=list(csv.DictReader(f))
assert len(rows)==5000 and len({x['order_id'] for x in rows})==5000
assert s['duplicates_removed']==25 and s['unknown_states']==20
for x in rows:
    expected=int(x['quantity'])*float(x['unit_price'])*(1-float(x['discount']))
    assert math.isclose(float(x['revenue']),expected,abs_tol=.01)
    assert math.isclose(float(x['profit']),expected-int(x['quantity'])*float(x['unit_cost']),abs_tol=.01)
c=sqlite3.connect(r/'data/ecommerce.db')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==5000
assert math.isclose(c.execute('SELECT SUM(revenue) FROM orders').fetchone()[0],s['revenue'],abs_tol=.01)
sql='\n'.join(line for line in (r/'sql/analysis.sql').read_text().splitlines() if not line.lstrip().startswith('--'))
for statement in sql.split(';'):
    if statement.strip(): c.execute(statement).fetchall()
c.close()
print('PASS: unique orders, cleaning counts, financial arithmetic, SQLite integrity, KPI reconciliation and all SQL queries')
