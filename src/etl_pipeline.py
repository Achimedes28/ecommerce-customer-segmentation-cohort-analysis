#!/usr/bin/env python3
"""
End-to-End ETL & Analytics Pipeline
Domain: E-Commerce Customer Segmentation & Cohort Retention Optimization
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
TABLEAU_DIR = os.path.join(BASE_DIR, "tableau")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(TABLEAU_DIR, exist_ok=True)

def run_pipeline():
    excel_path = os.path.join(BASE_DIR, "Data", "online_retail_II.xlsx")
    if not os.path.exists(excel_path):
        excel_path = os.path.join(BASE_DIR, "data", "online_retail_II.xlsx")
    
    print("1/5: Loading and consolidating raw transaction sheets...")
    df1 = pd.read_excel(excel_path, sheet_name="Year 2009-2010")
    df2 = pd.read_excel(excel_path, sheet_name="Year 2010-2011")
    df_raw = pd.concat([df1, df2], ignore_index=True)
    df_raw.columns = ['invoice_no', 'stock_code', 'description', 'quantity', 'invoice_date', 'unit_price', 'customer_id', 'country']

    print("2/5: Cleansing data (handling cancellations, nulls, returns)...")
    df_raw['invoice_no'] = df_raw['invoice_no'].astype(str).str.strip()
    df_raw['customer_id'] = pd.to_numeric(df_raw['customer_id'], errors='coerce')
    df_raw['invoice_date'] = pd.to_datetime(df_raw['invoice_date'])
    df_raw['description'] = df_raw['description'].astype(str).str.strip()

    df_clean = df_raw[
        (~df_raw['invoice_no'].str.startswith('C')) & 
        (df_raw['customer_id'].notna()) & 
        (df_raw['quantity'] > 0) & 
        (df_raw['unit_price'] > 0)
    ].copy()

    df_clean['customer_id'] = df_clean['customer_id'].astype(int)
    df_clean['total_sales'] = df_clean['quantity'] * df_clean['unit_price']
    df_clean['invoice_month'] = df_clean['invoice_date'].dt.to_period('M').dt.to_timestamp()

    print(f"   -> Valid Cleaned Records: {len(df_clean):,} | Unique Customers: {df_clean['customer_id'].nunique():,}")

    print("3/5: Computing Monthly Cohort Retention Matrix...")
    customer_cohort = df_clean.groupby('customer_id')['invoice_month'].min().reset_index()
    customer_cohort.rename(columns={'invoice_month': 'cohort_month'}, inplace=True)
    df_cohort = pd.merge(df_clean, customer_cohort, on='customer_id')

    df_cohort['cohort_index'] = (df_cohort['invoice_month'].dt.year - df_cohort['cohort_month'].dt.year) * 12 + (df_cohort['invoice_month'].dt.month - df_cohort['cohort_month'].dt.month)
    cohort_data = df_cohort.groupby(['cohort_month', 'cohort_index'])['customer_id'].apply(pd.Series.nunique).reset_index()
    cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_index', values='customer_id')
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)

    cohort_pivot.to_csv(os.path.join(METRICS_DIR, 'cohort_user_counts.csv'))
    retention_matrix.to_csv(os.path.join(METRICS_DIR, 'cohort_retention_rates.csv'))

    print("4/5: Computing RFM Behavioral Segmentation...")
    ref_date = df_clean['invoice_date'].max() + pd.Timedelta(days=1)
    rfm = df_clean.groupby('customer_id').agg({
        'invoice_date': lambda x: (ref_date - x.max()).days,
        'invoice_no': 'nunique',
        'total_sales': 'sum',
        'country': 'last'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency_days', 'frequency', 'monetary_value', 'country']

    rfm['r_score'] = pd.qcut(rfm['recency_days'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['m_score'] = pd.qcut(rfm['monetary_value'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

    def segment_customer(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']
        fm = (f + m) / 2
        if r >= 4 and fm >= 4:
            return 'Champions'
        elif r >= 3 and fm >= 3:
            return 'Loyal Customers'
        elif r >= 4 and fm <= 2:
            return 'New / Recent Customers'
        elif r >= 3 and fm <= 3:
            return 'Potential Loyalists'
        elif r <= 2 and fm >= 3:
            return 'At Risk'
        elif r <= 2 and fm <= 2:
            return 'Hibernating'
        else:
            return 'Lost / Others'

    rfm['segment'] = rfm.apply(segment_customer, axis=1)
    rfm.to_csv(os.path.join(DATA_DIR, 'customers_rfm_segmented.csv'), index=False)

    rfm_summary = rfm.groupby('segment').agg(
        customer_count=('customer_id', 'count'),
        total_revenue=('monetary_value', 'sum'),
        avg_recency=('recency_days', 'mean'),
        avg_frequency=('frequency', 'mean'),
        avg_monetary=('monetary_value', 'mean')
    ).reset_index()
    rfm_summary['pct_customers'] = (rfm_summary['customer_count'] / len(rfm)) * 100
    rfm_summary['pct_revenue'] = (rfm_summary['total_revenue'] / rfm['monetary_value'].sum()) * 100
    rfm_summary = rfm_summary.sort_values(by='total_revenue', ascending=False)
    rfm_summary.to_csv(os.path.join(METRICS_DIR, 'rfm_segment_summary.csv'), index=False)

    print("5/5: Populating Indexed SQLite Database...")
    db_path = os.path.join(DATA_DIR, 'online_retail_analytics.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    df_clean['invoice_date_str'] = df_clean['invoice_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_clean[['invoice_no', 'stock_code', 'description', 'quantity', 'invoice_date_str', 'unit_price', 'total_sales', 'customer_id', 'country']].to_sql(
        'fact_transactions', conn, if_exists='replace', index=False
    )
    rfm.to_sql('dim_customers_rfm', conn, if_exists='replace', index=False)
    cohort_data.to_sql('fact_cohort_activity', conn, if_exists='replace', index=False)

    cur.execute('CREATE INDEX IF NOT EXISTS idx_trans_cust ON fact_transactions(customer_id);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_trans_date ON fact_transactions(invoice_date_str);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_rfm_cust ON dim_customers_rfm(customer_id);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_rfm_seg ON dim_customers_rfm(segment);')

    conn.commit()
    conn.close()
    print("ETL Pipeline Finished Successfully!")

if __name__ == "__main__":
    run_pipeline()
