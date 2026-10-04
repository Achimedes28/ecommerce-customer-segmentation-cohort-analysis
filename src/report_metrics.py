#!/usr/bin/env python3
"""
Single source of truth for the figures quoted in the README, PDF report and slide deck.

Every number is computed from the committed analysis outputs:
  data/customers_rfm_segmented.csv  (one row per customer, RFM scores and segment)
  metrics/cohort_user_counts.csv    (active customers per cohort and month offset)

Figures that come from the full raw dataset (row counts before and after cleaning)
are constants recorded from src/etl_pipeline.py output, because the raw file is not committed.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")

# Recorded from src/etl_pipeline.py on online_retail_II.xlsx (both sheets).
RAW_ROWS = 1_067_371
CLEAN_ROWS = 805_549

SEGMENT_ORDER = [
    "Champions", "Loyal Customers", "Potential Loyalists", "New / Recent Customers",
    "At Risk", "Hibernating", "Lost",
]


def load_metrics():
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers_rfm_segmented.csv"))
    counts = pd.read_csv(os.path.join(METRICS_DIR, "cohort_user_counts.csv"), index_col=0)
    counts.index = pd.to_datetime(counts.index)
    counts.columns = counts.columns.astype(int)

    revenue = customers["monetary_value"].sum()
    n_customers = len(customers)
    orders = customers["frequency"].sum()

    seg = (customers.groupby("segment")
           .agg(customers=("customer_id", "count"),
                revenue=("monetary_value", "sum"),
                recency=("recency_days", "mean"),
                orders=("frequency", "mean"),
                spend=("monetary_value", "mean"))
           .reindex(SEGMENT_ORDER))
    seg["pct_customers"] = seg["customers"] / n_customers
    seg["pct_revenue"] = seg["revenue"] / revenue

    def retention(k):
        observed = counts[k].notna()
        return counts.loc[observed, k].sum() / counts.loc[observed, 0].sum()

    retention_curve = {k: retention(k) for k in range(1, 13)}
    cohort_m1 = (counts[1] / counts[0]).dropna()

    core = seg.loc[["Champions", "Loyal Customers"]]
    dormant = seg.loc[["Hibernating", "Lost"]]
    country_rev = customers.groupby("country")["monetary_value"].sum().sort_values(ascending=False)

    return {
        "raw_rows": RAW_ROWS,
        "clean_rows": CLEAN_ROWS,
        "period": "Dec 2009 – Dec 2011",
        "revenue": revenue,
        "customers": n_customers,
        "countries": customers["country"].nunique(),
        "orders": int(orders),
        "aov": revenue / orders,
        "revenue_per_customer": revenue / n_customers,
        "orders_per_customer": orders / n_customers,
        "median_recency": customers["recency_days"].median(),
        "m1": retention_curve[1],
        "m1_churn": 1 - retention_curve[1],
        "retention_curve": retention_curve,
        "retention_min_m1_m12": min(retention_curve.values()),
        "retention_max_m1_m12": max(retention_curve.values()),
        "cohort_m1": cohort_m1,
        "seg": seg,
        "core_pct_customers": core["pct_customers"].sum(),
        "core_pct_revenue": core["pct_revenue"].sum(),
        "core_revenue": core["revenue"].sum(),
        "core_customers": int(core["customers"].sum()),
        "dormant_pct_customers": dormant["pct_customers"].sum(),
        "dormant_pct_revenue": dormant["pct_revenue"].sum(),
        "uk_share": country_rev.iloc[0] / revenue,
    }


def money(x, decimals=0):
    return f"£{x:,.{decimals}f}"


def money_m(x):
    return f"£{x / 1e6:.2f}M"


def pct(x, decimals=1):
    return f"{x * 100:.{decimals}f}%"


if __name__ == "__main__":
    m = load_metrics()
    for k, v in m.items():
        if k not in ("seg", "cohort_m1", "retention_curve"):
            print(f"{k:24s} {v}")
    print(m["seg"].round(3).to_string())
    print({k: round(v, 3) for k, v in m["retention_curve"].items()})
    print(m["cohort_m1"].round(3).to_string())
