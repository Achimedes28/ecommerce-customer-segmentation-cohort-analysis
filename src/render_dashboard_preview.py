#!/usr/bin/env python3
"""
Render static previews of the three Power BI report pages (1280x720 canvas)
from powerbi/data, so the README can show the dashboard layout on GitHub.
Replace these with real screenshots once the .pbix is built.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PBI_DATA = os.path.join(BASE_DIR, "powerbi", "data")
OUT_DIR = os.path.join(BASE_DIR, "powerbi", "preview")
os.makedirs(OUT_DIR, exist_ok=True)

# Tokens shared with powerbi/theme/minimal_light.json
PAGE = "#F8FAFC"
CARD = "#FFFFFF"
BORDER = "#E2E8F0"
INK = "#0F172A"
INK_2 = "#475569"
INK_3 = "#94A3B8"
GRID = "#F1F5F9"
ACCENT = "#2A78D6"
NEUTRAL = "#CBD5E1"
SEQ = LinearSegmentedColormap.from_list("seq", ["#EEF5FD", "#9EC5F4", "#3987E5", "#1C5CAB", "#0D366B"])

W, H = 1280, 720
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
    "axes.edgecolor": BORDER,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

customers = pd.read_csv(os.path.join(PBI_DATA, "dim_customer.csv"))
segments = pd.read_csv(os.path.join(PBI_DATA, "dim_segment.csv"))
cohort = pd.read_csv(os.path.join(PBI_DATA, "fact_cohort.csv"), parse_dates=["cohort_month", "activity_month"])


def new_page(title, subtitle, active_tab):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=200, facecolor=PAGE)
    fig.text(24 / W, 1 - 34 / H, title, fontsize=15, weight="bold", color=INK, va="center")
    fig.text(24 / W, 1 - 56 / H, subtitle, fontsize=8.5, color=INK_2, va="center")
    x = W - 24
    for tab in reversed(["Overview", "Cohort Retention", "RFM Segments"]):
        width = 14 + len(tab) * 6.2
        x -= width
        active = tab == active_tab
        fig.patches.append(FancyBboxPatch((x / W, 1 - 52 / H), width / W, 24 / H,
                                          boxstyle="round,pad=0,rounding_size=0.006",
                                          transform=fig.transFigure, zorder=-10,
                                          facecolor=INK if active else CARD, edgecolor=INK if active else BORDER, lw=0.8))
        fig.text((x + width / 2) / W, 1 - 40 / H, tab, fontsize=7.5, ha="center", va="center",
                 color=CARD if active else INK_2)
        x -= 8
    return fig


def card(fig, x, y, w, h, title=None, left=16, bottom=14, top=None):
    """Draw a card at pixel coords (top-left origin); return the plot rect inside it.

    left/bottom reserve room for tick labels inside the card.
    """
    fig.patches.append(FancyBboxPatch((x / W, 1 - (y + h) / H), w / W, h / H,
                                      boxstyle="round,pad=0,rounding_size=0.008",
                                      transform=fig.transFigure, facecolor=CARD, edgecolor=BORDER, lw=0.8, zorder=-10))
    if title:
        fig.text((x + 16) / W, 1 - (y + 20) / H, title, fontsize=9, weight="bold", color=INK, va="center")
    if top is None:
        top = 40 if title else 12
    return [(x + left) / W, 1 - (y + h - bottom) / H, (w - left - 16) / W, (h - top - bottom) / H]


def kpi(fig, x, y, w, h, label, value, note=None):
    card(fig, x, y, w, h)
    fig.text((x + 16) / W, 1 - (y + 22) / H, label, fontsize=8, color=INK_2, va="center")
    fig.text((x + 16) / W, 1 - (y + 52) / H, value, fontsize=19, weight="bold", color=INK, va="center")
    if note:
        fig.text((x + 16) / W, 1 - (y + 78) / H, note, fontsize=7.5, color=INK_3, va="center")


def clean(ax, grid_axis="y"):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_facecolor(CARD)


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, facecolor=PAGE)
    plt.close(fig)
    print("saved", os.path.relpath(path, BASE_DIR))


# ---- shared numbers ---------------------------------------------------------
revenue = customers["monetary_value"].sum()
n_customers = len(customers)
orders = customers["frequency"].sum()


def retention_at(k):
    s = cohort[cohort["month_index"] == k]
    return s["active_customers"].sum() / s["cohort_size"].sum()


seg = (customers.groupby("segment")
       .agg(customers=("customer_id", "count"), revenue=("monetary_value", "sum"),
            recency=("recency_days", "mean"), frequency=("frequency", "mean"))
       .reset_index().merge(segments, on="segment").sort_values("segment_order"))
seg["rev_share"] = seg["revenue"] / revenue
seg["cust_share"] = seg["customers"] / n_customers
core = seg[seg["segment_group"] == "Core"]

KW = (W - 48 - 3 * 12) / 4

# ---- Page 1: Overview -------------------------------------------------------
fig = new_page("Customer Retention & Segmentation", "Online retail transactions, Dec 2009 - Dec 2011  |  5,878 customers", "Overview")
tiles = [
    ("Total revenue", f"£{revenue / 1e6:.2f}M", "Completed orders, net of cancellations"),
    ("Customers", f"{n_customers:,}", f"{customers['country'].nunique()} countries"),
    ("Revenue per customer", f"£{revenue / n_customers:,.0f}", f"{orders / n_customers:.1f} orders on average"),
    ("Avg order value", f"£{revenue / orders:,.0f}", f"{orders:,} orders"),
    ("Month-1 retention", f"{retention_at(1):.1%}", "Customer-weighted, all cohorts"),
]
tw = (W - 48 - 4 * 12) / 5
for i, (label, value, note) in enumerate(tiles):
    kpi(fig, 24 + i * (tw + 12), 80, tw, 96, label, value, note)

monthly = (cohort.assign(kind=np.where(cohort["month_index"] == 0, "new", "returning"))
           .pivot_table(index="activity_month", columns="kind", values="active_customers", aggfunc="sum", fill_value=0))
ax = fig.add_axes(card(fig, 24, 188, 780, 508, "Active customers per month: new vs returning", left=52, bottom=34))
x = np.arange(len(monthly))
ax.bar(x, monthly["returning"], color=ACCENT, width=0.72, label="Returning")
ax.bar(x, monthly["new"], bottom=monthly["returning"] + 8, color=NEUTRAL, width=0.72, label="New")
ax.set_xticks(x[::3])
ax.set_xticklabels(monthly.index[::3].strftime("%b %y"))
clean(ax)
ax.legend(loc="upper left", frameon=False, fontsize=7.5, ncol=2)
peak = monthly.sum(axis=1).idxmax()
pi = list(monthly.index).index(peak)
ax.annotate(f"Peak {int(monthly.loc[peak].sum()):,}", (pi, monthly.loc[peak].sum() + 8), xytext=(0, 6),
            textcoords="offset points", ha="center", fontsize=7.5, color=INK)

country = customers.groupby("country")["monetary_value"].sum().sort_values(ascending=False)
top = country.head(8)[::-1] / revenue
ax = fig.add_axes(card(fig, 816, 188, 440, 508, "Revenue share by country (top 8)", left=110))
ax.barh(top.index, top.values, color=[ACCENT if c == "United Kingdom" else NEUTRAL for c in top.index], height=0.6)
for i, v in enumerate(top.values):
    ax.text(v + 0.01, i, f"{v:.1%}", va="center", fontsize=7.5, color=INK)
ax.set_xlim(0, 1.0)
ax.set_xticks([])
clean(ax, grid_axis=None)
ax.spines["bottom"].set_visible(False)
save(fig, "01_overview.png")

# ---- Page 2: Cohort Retention -----------------------------------------------
fig = new_page("Cohort Retention", "Share of each acquisition cohort that purchased again N months later", "Cohort Retention")
for i, k in enumerate([1, 3, 6, 12]):
    kpi(fig, 24 + i * (KW + 12), 80, KW, 96, f"Month-{k} retention", f"{retention_at(k):.1%}",
        "First month after acquisition" if k == 1 else None)

matrix = cohort[cohort["month_index"] <= 12].pivot(index="cohort_month", columns="month_index", values="retention_rate").iloc[:13]
ax = fig.add_axes(card(fig, 24, 188, 800, 508, "Retention matrix: cohort x months since first purchase", left=76, top=62))
shown = matrix.copy()
shown[0] = np.nan  # month 0 is always 100%; leave it out of the colour scale
ax.imshow(shown.values, cmap=SEQ, vmin=0, vmax=0.5, aspect="auto")
for (r, c), v in np.ndenumerate(matrix.values):
    if np.isnan(v):
        continue
    ax.text(c, r, "100%" if c == 0 else f"{v:.0%}", ha="center", va="center", fontsize=6.5,
            color=INK_2 if c == 0 else (CARD if v >= 0.3 else INK))
ax.set_xticks(range(matrix.shape[1]))
ax.set_xticklabels([f"M{c}" for c in matrix.columns])
ax.set_yticks(range(matrix.shape[0]))
ax.set_yticklabels(matrix.index.strftime("%b %Y"))
ax.xaxis.tick_top()
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

curve = cohort[(cohort["month_index"] > 0) & (cohort["month_index"] <= 12)].groupby("month_index")[["active_customers", "cohort_size"]].sum()
curve = curve["active_customers"] / curve["cohort_size"]
ax = fig.add_axes(card(fig, 836, 188, 420, 508, "Average retention curve (M1-M12)", left=48, bottom=34))
ax.plot(curve.index, curve.values, color=ACCENT, lw=2, marker="o", ms=4)
ax.set_ylim(0, 0.35)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
ax.set_xticks(curve.index)
ax.set_xticklabels([f"M{i}" for i in curve.index])
clean(ax)
ax.annotate(f"{curve.loc[1]:.1%}", (1, curve.loc[1]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=7.5, color=INK)
ax.text(0.02, 0.06, "About 3 in 4 customers do not return\nin the month after their first order.",
        transform=ax.transAxes, fontsize=7.5, color=INK_2)
save(fig, "02_cohort_retention.png")

# ---- Page 3: RFM Segments ---------------------------------------------------
fig = new_page("RFM Segments", "Recency, frequency and monetary scores (quintiles) grouped into seven segments", "RFM Segments")
kpis3 = [
    ("Core revenue share", f"{core['rev_share'].sum():.1%}", "Champions + Loyal Customers"),
    ("Core customer share", f"{core['cust_share'].sum():.1%}", f"{core['customers'].sum():,} customers"),
    ("At Risk revenue", f"£{seg.loc[seg.segment == 'At Risk', 'revenue'].sum() / 1e6:.2f}M", "Win-back priority"),
    ("Median recency", f"{customers['recency_days'].median():.0f} days", "Days since last order"),
]
for i, (label, value, note) in enumerate(kpis3):
    kpi(fig, 24 + i * (KW + 12), 80, KW, 96, label, value, note)

ax = fig.add_axes(card(fig, 24, 188, 520, 508, "Revenue share vs customer share", left=150))
order = seg.iloc[::-1]
y = np.arange(len(order))
ax.barh(y + 0.19, order["rev_share"], height=0.36, color=ACCENT, label="Revenue share")
ax.barh(y - 0.19, order["cust_share"], height=0.36, color=NEUTRAL, label="Customer share")
for i, (r, c) in enumerate(zip(order["rev_share"], order["cust_share"])):
    ax.text(r + 0.01, i + 0.19, f"{r:.1%}", va="center", fontsize=7, color=INK)
    ax.text(c + 0.01, i - 0.19, f"{c:.1%}", va="center", fontsize=7, color=INK_2)
ax.set_yticks(y)
ax.set_yticklabels(order["segment"])
ax.set_xlim(0, 0.8)
ax.set_xticks([])
clean(ax, grid_axis=None)
ax.spines["bottom"].set_visible(False)
ax.legend(loc="lower right", frameon=False, fontsize=7.5)

ax = fig.add_axes(card(fig, 556, 188, 700, 508, "Segment scorecard"))
ax.axis("off")
cols = ["Segment", "Customers", "Revenue", "Recency", "Orders", "Recommended action"]
xs = [0.0, 0.24, 0.35, 0.46, 0.575, 0.68]
for xpos, col in zip(xs, cols):
    ax.text(xpos, 0.97, col, fontsize=7.5, weight="bold", color=INK_2, va="top", ha="left")
ax.axhline(0.92, color=BORDER, lw=0.8)
row_h = 0.125
for i, r in enumerate(seg.itertuples()):
    yy = 0.86 - i * row_h
    vals = [r.segment, f"{r.customers:,}", f"£{r.revenue / 1e6:.2f}M", f"{r.recency:.0f} d", f"{r.frequency:.1f}"]
    for xpos, v in zip(xs, vals):
        ax.text(xpos, yy, v, fontsize=7.5, color=INK, va="top")
    words, line, lines = r.recommended_action.split(), "", []
    for w_ in words:
        if len(line) + len(w_) > 30:
            lines.append(line)
            line = w_
        else:
            line = f"{line} {w_}".strip()
    lines.append(line)
    ax.text(xs[-1], yy, "\n".join(lines), fontsize=7, color=INK_2, va="top", linespacing=1.3)
    ax.axhline(yy - row_h + 0.02, color=GRID, lw=0.8)
ax.set_ylim(0, 1)
ax.set_xlim(0, 1)
save(fig, "03_rfm_segments.png")
