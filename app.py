from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='Commerce Analytics',page_icon='📊',layout='wide')
st.title('E-Commerce Sales & Customer Analytics')
st.caption('Portfolio project • Synthetic transactions • INR • 2024–2025')
@st.cache_data
def load():
    return pd.read_csv(ROOT/'data/clean_orders.csv',parse_dates=['order_date'])
df=load()
st.sidebar.header('Filter transactions')
categories=st.sidebar.multiselect('Category',sorted(df.category.unique()),default=sorted(df.category.unique()))
states=st.sidebar.multiselect('State',sorted(df.state.unique()),default=sorted(df.state.unique()))
dates=st.sidebar.date_input('Date range',value=(df.order_date.min().date(),df.order_date.max().date()),min_value=df.order_date.min().date(),max_value=df.order_date.max().date())
if len(dates)!=2:
    st.info('Select a start and end date.'); st.stop()
f=df[df.category.isin(categories)&df.state.isin(states)&df.order_date.dt.date.between(*dates)].copy()
if f.empty:
    st.warning('No orders match these filters.'); st.stop()
revenue=f.revenue.sum(); profit=f.profit.sum()
cols=st.columns(4)
for c,label,value in zip(cols,['Revenue','Profit','Orders','Average order value'],[f'₹{revenue:,.0f}',f'₹{profit:,.0f}',f'{f.order_id.nunique():,}',f'₹{revenue/f.order_id.nunique():,.0f}']): c.metric(label,value)
st.metric('Profit margin',f'{profit/revenue*100:.1f}%')
f['month']=f.order_date.dt.to_period('M').astype(str)
a,b=st.columns(2)
with a:
    st.subheader('Monthly sales and profit'); st.line_chart(f.groupby('month')[['revenue','profit']].sum())
with b:
    st.subheader('Category performance'); st.bar_chart(f.groupby('category')[['revenue','profit']].sum())
a,b=st.columns(2)
with a:
    st.subheader('State revenue'); st.bar_chart(f.groupby('state').revenue.sum())
with b:
    st.subheader('Top products by revenue'); st.bar_chart(f.groupby('product').revenue.sum().sort_values(ascending=False).head(10))
st.subheader('Customer purchase frequency')
counts=f.groupby('customer_id').order_id.nunique()
st.write(f'{(counts>1).sum():,} repeat customers / {len(counts):,} customers ({(counts>1).mean()*100:.1f}%) in the selected period.')
st.caption('Repeat means more than one order within the current filters; this is not a cohort retention metric.')
st.subheader('Filtered transactions'); st.dataframe(f,hide_index=True,use_container_width=True)
st.download_button('Download filtered CSV',f.to_csv(index=False).encode(),'filtered_orders.csv','text/csv')
