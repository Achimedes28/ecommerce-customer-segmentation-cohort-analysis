#!/usr/bin/env python3
"""
Build the Power BI star-schema tables from the analysis outputs.

Inputs : data/customers_rfm_segmented.csv, metrics/cohort_user_counts.csv
Outputs: powerbi/data/{dim_customer,dim_segment,fact_cohort}.csv
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")
OUT_DIR = os.path.join(BASE_DIR, "powerbi", "data")
os.makedirs(OUT_DIR, exist_ok=True)

# Segment order runs from most to least valuable; actions mirror the README playbook.
SEGMENTS = [
    ("Champions", 1, "Core", "VIP perks and early access, no blanket discounts"),
    ("Loyal Customers", 2, "Core", "Loyalty tiers and cross-sell recommendations"),
    ("Potential Loyalists", 3, "Grow", "Nudge toward 3rd and 5th order milestones"),
    ("New / Recent Customers", 4, "Grow", "14-day post-purchase onboarding flow"),
    ("At Risk", 5, "Win back", "Re-engagement trigger at 60 days without an order"),
    ("Hibernating", 6, "Dormant", "Low-cost seasonal reactivation only"),
    ("Lost", 7, "Dormant", "Suppress from paid campaigns"),
]


def build_dim_segment():
    return pd.DataFrame(SEGMENTS, columns=["segment", "segment_order", "segment_group", "recommended_action"])


def build_dim_customer():
    df = pd.read_csv(os.path.join(DATA_DIR, "customers_rfm_segmented.csv"))
    df["monetary_value"] = df["monetary_value"].round(2)
    return df


def build_fact_cohort():
    counts = pd.read_csv(os.path.join(METRICS_DIR, "cohort_user_counts.csv"), index_col=0)
    counts.index = pd.to_datetime(counts.index)
    long = (
        counts.reset_index()
        .melt(id_vars="cohort_month", var_name="month_index", value_name="active_customers")
        .dropna(subset=["active_customers"])
    )
    long["month_index"] = long["month_index"].astype(int)
    long["active_customers"] = long["active_customers"].astype(int)
    long["cohort_size"] = long["cohort_month"].map(counts.iloc[:, 0]).astype(int)
    long["activity_month"] = long.apply(
        lambda r: r["cohort_month"] + pd.DateOffset(months=r["month_index"]), axis=1
    )
    long["retention_rate"] = (long["active_customers"] / long["cohort_size"]).round(4)
    long = long.sort_values(["cohort_month", "month_index"])
    for col in ("cohort_month", "activity_month"):
        long[col] = long[col].dt.strftime("%Y-%m-%d")
    return long[["cohort_month", "month_index", "activity_month", "cohort_size", "active_customers", "retention_rate"]]


if __name__ == "__main__":
    dim_segment = build_dim_segment()
    dim_customer = build_dim_customer()
    unknown = set(dim_customer["segment"]) - set(dim_segment["segment"])
    if unknown:
        raise SystemExit(f"Segments missing from dim_segment: {sorted(unknown)}")
    fact_cohort = build_fact_cohort()

    dim_segment.to_csv(os.path.join(OUT_DIR, "dim_segment.csv"), index=False)
    dim_customer.to_csv(os.path.join(OUT_DIR, "dim_customer.csv"), index=False)
    fact_cohort.to_csv(os.path.join(OUT_DIR, "fact_cohort.csv"), index=False)
    print(f"dim_customer: {len(dim_customer):,} rows | dim_segment: {len(dim_segment)} rows | fact_cohort: {len(fact_cohort)} rows")
