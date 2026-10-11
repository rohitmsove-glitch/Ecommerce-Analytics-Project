import csv, random
from pathlib import Path
from datetime import date, timedelta
ROOT=Path(__file__).resolve().parent

def generate():
    rng=random.Random(42)
    products=[('Laptop','Electronics',55000,41000),('Headphones','Electronics',2500,1400),('Shirt','Fashion',1200,650),('Shoes','Fashion',3000,1700),('Chair','Home',4500,3000),('Lamp','Home',900,520)]
    rows=[]
    for i in range(1,5001):
        dt=date(2024,1,1)+timedelta(days=rng.randrange(731))
        name,cat,price,cost=rng.choice(products)
        qty=rng.randint(1,4); discount=rng.choice([0,.05,.10,.15,.20])
        sales=round(price*qty*(1-discount),2)
        rows.append(dict(order_id=f'O{i:05}',order_date=dt.isoformat(),customer_id=f'C{rng.randint(1,1000):04}',product=name,category=cat,state=rng.choice(['Maharashtra','Gujarat','Karnataka','Delhi','Tamil Nadu']),quantity=qty,unit_price=price,unit_cost=cost,discount=discount,revenue=sales,profit=round(sales-cost*qty,2)))
    rows.sort(key=lambda x:x['order_date'])
    # Deliberate quality issues for the cleaning demonstration.
    raw=[dict(r) for r in rows]
    for r in raw[:20]: r['state']=''
    raw+= [dict(r) for r in raw[100:125]]
    with (ROOT/'data/raw_orders.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(raw)
    print(f'Generated {len(raw)} synthetic rows')
if __name__=='__main__': generate()
