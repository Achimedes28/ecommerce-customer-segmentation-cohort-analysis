#!/usr/bin/env python3
"""
Generate Clean Minimalist High-Resolution Charts (300 DPI)
Theme: Professional Minimalist (Light, crisp, McKinsey/Bain/Tech style)
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = "/Users/novaldiramadhanwaluyo/Desktop/Certificate and portfolio/Portfolio/Portfolio Data Analyst/E-Commerce Customer Segmentation & Cohort Analysis"
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(VIZ_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# PLOT STYLING (Professional Minimalist Light)
# -----------------------------------------------------------------------------
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#F1F5F9'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.6

# 1. COHORT HEATMAP
retention_matrix = pd.read_csv(os.path.join(METRICS_DIR, 'cohort_retention_rates.csv'), index_col=0)
retention_matrix.index = pd.to_datetime(retention_matrix.index).strftime('%Y-%m')

# Take first 12 cohorts and 12 cohort periods for clean aspect ratio
cohort_sub = retention_matrix.iloc[:12, :13]

plt.figure(figsize=(10, 5.2), dpi=300, facecolor='#FFFFFF')
ax = sns.heatmap(
    cohort_sub,
    annot=True,
    fmt='.1%',
    cmap='Blues',
    vmin=0.0,
    vmax=0.45,
    cbar_kws={'label': 'Retention Rate'},
    linewidths=1.0,
    linecolor='#FFFFFF',
    annot_kws={'size': 7.5, 'weight': 'bold', 'color': '#0F172A'}
)
plt.title('Monthly Customer Cohort Retention Rate (%)', fontsize=12, weight='bold', color='#0F172A', pad=12)
plt.xlabel('Cohort Period (Months Since First Purchase)', fontsize=9, weight='bold', color='#475569', labelpad=8)
plt.ylabel('Cohort Acquisition Month', fontsize=9, weight='bold', color='#475569', labelpad=8)
plt.tick_params(axis='both', which='major', labelsize=8, colors='#334155')
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, '01_cohort_retention_heatmap.png'), dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
plt.close()

# 2. RFM REVENUE VS CUSTOMERS
rfm_summary = pd.read_csv(os.path.join(METRICS_DIR, 'rfm_segment_summary.csv'))

fig, ax1 = plt.subplots(figsize=(10, 5.2), dpi=300, facecolor='#FFFFFF')
x = np.arange(len(rfm_summary))
width = 0.4

# Bars for Revenue
bars = ax1.bar(x - width/2, rfm_summary['pct_revenue'], width=width, label='% Total Revenue', color='#2563EB', edgecolor='none', alpha=0.9, zorder=3)
ax1.set_ylabel('% Total Revenue Contribution', fontsize=9, weight='bold', color='#2563EB', labelpad=8)
ax1.set_xticks(x)
ax1.set_xticklabels(rfm_summary['segment'], rotation=25, ha='right', fontsize=8.5, weight='bold', color='#0F172A')
ax1.tick_params(axis='y', labelsize=8, colors='#2563EB')
ax1.set_ylim(0, 50)
ax1.grid(axis='y', zorder=0, alpha=0.6)

# Direct data labels on bars
for bar in bars:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%', ha='center', va='bottom', fontsize=7.5, weight='bold', color='#1E40AF')

# Bars for Customer Share
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, rfm_summary['pct_customers'], width=width, label='% Customer Base', color='#94A3B8', edgecolor='none', alpha=0.85, zorder=3)
ax2.set_ylabel('% Total Customer Base', fontsize=9, weight='bold', color='#64748B', labelpad=8)
ax2.tick_params(axis='y', labelsize=8, colors='#64748B')
ax2.set_ylim(0, 50)
ax2.grid(False)

for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%', ha='center', va='bottom', fontsize=7.5, weight='bold', color='#475569')

plt.title('Customer Segments: Revenue Contribution vs Customer Share (Pareto Dynamic)', fontsize=12, weight='bold', color='#0F172A', pad=12)
fig.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, '02_rfm_revenue_vs_customers.png'), dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
plt.close()

# 3. MONTHLY REVENUE & ORDER GROWTH
df_clean = pd.read_sql('SELECT invoice_date_str, total_sales, invoice_no FROM fact_transactions', 
                       sqlite3_conn := __import__('sqlite3').connect(os.path.join(DATA_DIR, 'online_retail_analytics.db')))
sqlite3_conn.close()

df_clean['invoice_month'] = df_clean['invoice_date_str'].str.slice(0, 7)
monthly = df_clean.groupby('invoice_month').agg(
    revenue=('total_sales', 'sum'),
    orders=('invoice_no', 'nunique')
).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5.2), dpi=300, facecolor='#FFFFFF')
ax1.plot(monthly['invoice_month'], monthly['revenue'] / 1e6, color='#0284C7', marker='o', markersize=4, linewidth=2.2, label='Revenue (£M)', zorder=4)
ax1.fill_between(monthly['invoice_month'], monthly['revenue'] / 1e6, color='#E0F2FE', alpha=0.6, zorder=3)
ax1.set_ylabel('Monthly Revenue (£ Millions)', fontsize=9, weight='bold', color='#0284C7', labelpad=8)
ax1.set_xticklabels(monthly['invoice_month'], rotation=45, ha='right', fontsize=8, color='#334155')
ax1.tick_params(axis='y', labelsize=8, colors='#0284C7')
ax1.set_ylim(0, 2.0)
ax1.grid(axis='both', zorder=0, alpha=0.6)

ax2 = ax1.twinx()
ax2.plot(monthly['invoice_month'], monthly['orders'], color='#F59E0B', linestyle='--', marker='s', markersize=3.5, linewidth=1.8, label='Orders Count', zorder=4)
ax2.set_ylabel('Monthly Completed Orders', fontsize=9, weight='bold', color='#D97706', labelpad=8)
ax2.tick_params(axis='y', labelsize=8, colors='#D97706')
ax2.grid(False)

plt.title('Monthly E-Commerce Revenue (£M) & Order Volume Trajectory', fontsize=12, weight='bold', color='#0F172A', pad=12)
fig.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, '03_monthly_revenue_growth.png'), dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
plt.close()

print('Clean minimalist charts generated successfully!')
