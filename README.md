# E-Commerce Customer Segmentation and Cohort Retention

Analysis of two years of transactions from a UK-based online retailer (UCI Online Retail II dataset).

The project follows a case brief ([`Project Brief - Customer Lifetime Value & Retention Optimization.pdf`](Project%20Brief%20-%20Customer%20Lifetime%20Value%20%26%20Retention%20Optimization.pdf)). In the scenario, the retailer's customer acquisition cost has risen 25% over 12 months while marketing still relies on untargeted mass promotions. The task is to answer two questions:

1. How many new customers come back after their first purchase, and when do most of them stop buying?
2. Which customer groups generate most of the revenue, and which groups are worth a retention or win-back effort?

**Tools:** SQL (SQLite), Python (pandas, seaborn), Tableau

## Data

- Source: [Online Retail II, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- Period: December 2009 to 9 December 2011
- About 1.06 million raw rows, reduced to 805,549 after cleaning
- 5,878 customers with a customer ID, £17.74M in revenue after cleaning

Cleaning steps:

- Removed rows without a customer ID, because they cannot be assigned to a cohort or an RFM segment
- Removed cancelled invoices (invoice numbers starting with "C") and rows with zero or negative quantity or price
- Calculated `total_sales = quantity * unit_price`

The CAC increase comes from the brief, not from the data. The dataset itself has no marketing spend, acquisition channel or margin data, so this analysis looks at customer behaviour and revenue only, not at campaign cost or profit.

## Findings

### 1. Most customers do not return in the month after their first purchase

![Cohort retention heatmap](visualizations/01_cohort_retention_heatmap.png)

Across the 24 monthly cohorts that have a month-1 value, on average only **21%** of customers bought again in the month after their first order. Retention then stays roughly flat around 20% for the next few months and settles at about 15 to 18% by month 6 to 12.

So the biggest loss happens right after the first order. Customers who make it past the first few months tend to keep buying.

One exception: the December 2009 cohort retains much better (35% in month 1, 38% in month 12). This is most likely because the data starts in December 2009, so that "cohort" includes existing customers who had been buying before the data begins. I excluded it when reading the general pattern.

### 2. A small group of customers brings in most of the revenue

![RFM revenue vs customer share](visualizations/02_rfm_revenue_vs_customers.png)

Customers were scored 1 to 5 on recency, frequency and monetary value using quintiles (pandas `qcut` in `etl_pipeline.py`; `sql/03_rfm_segmentation.sql` is the equivalent SQL version with `NTILE(5)`), with 10 December 2011 as the reference date, and then grouped into segments.

| Segment | Customers | % of customers | Revenue | % of revenue | Avg days since last order | Avg orders | Avg spend |
|---|---:|---:|---:|---:|---:|---:|---:|
| Champions | 1,324 | 22.5% | £12.24M | 69.0% | 20 | 16.9 | £9,246 |
| Loyal Customers | 1,207 | 20.5% | £2.78M | 15.7% | 74 | 5.8 | £2,302 |
| At Risk | 683 | 11.6% | £1.71M | 9.6% | 364 | 5.3 | £2,501 |
| Hibernating | 1,377 | 23.4% | £0.39M | 2.2% | 466 | 1.2 | £286 |
| Potential Loyalists | 635 | 10.8% | £0.31M | 1.7% | 84 | 1.9 | £487 |
| Lost | 287 | 4.9% | £0.20M | 1.1% | 396 | 2.3 | £692 |
| New / Recent | 365 | 6.2% | £0.11M | 0.6% | 29 | 1.4 | £309 |

- Champions and Loyal Customers are 43% of customers but 85% of revenue.
- The At Risk group used to buy often (5.3 orders on average) but has not ordered for about a year. Together they spent £1.71M, which makes them the most obvious win-back target.
- Hibernating is the largest group by headcount (23%) but contributes only 2% of revenue.

### 3. Revenue is seasonal

![Monthly revenue](visualizations/03_monthly_revenue_growth.png)

Revenue rises from September and peaks in November in both 2010 and 2011, which fits a retailer that sells a lot of gift items. December 2011 looks low only because the data stops on 9 December.

## Recommendations

These are directional, since the data does not include cost or campaign results.

1. **Focus on the second purchase.** The largest drop happens in the first month. A follow-up offer or product recommendation within a few weeks of the first order targets exactly that gap.
2. **Run a win-back campaign for At Risk customers.** They have a proven buying history and a combined £1.71M in past spend. Even a small reactivation rate would be worth more than a campaign aimed at Hibernating customers.
3. **Keep Champions without heavy discounts.** They already buy often, so early access or service perks are a cheaper way to keep them than price cuts.
4. **Plan stock and campaigns around September to November**, when demand is highest.

## Limitations

- No marketing cost, channel or margin data, so the recommendations cannot be costed.
- About a quarter of the raw rows have no customer ID and were excluded. Revenue figures here only cover identified customers.
- The data ends on 9 December 2011, so the latest cohorts have only a few months of history.
- RFM segments depend on the chosen thresholds. Different cut-offs would move some customers between segments.

## Repository

```
├── Data/
│   ├── customers_rfm_segmented.csv            one row per customer with RFM scores and segment
│   └── cleaned_transactions_sample100k.csv    first 100,000 cleaned rows (Dec 2009 to Mar 2010), a preview only
├── sql/
│   ├── 01_schema_and_views.sql                tables, indexes and summary views
│   ├── 02_cohort_analysis.sql                 cohort retention query
│   └── 03_rfm_segmentation.sql                RFM scoring with NTILE and segment rules
├── src/
│   ├── etl_pipeline.py                        cleaning, cohorts, RFM scoring, SQLite database
│   ├── generate_minimalist_visualizations.py  charts in visualizations/
│   └── build_report_and_deck.py               PDF report and PPTX deck, all figures read from metrics/
├── metrics/                                   cohort retention rates, cohort sizes, RFM summary
├── visualizations/                            charts used in this README
├── tableau/online_retail_analytics.tds        Tableau data source for the SQLite database
├── presentations/                             executive presentation (PPTX)
├── reports/                                   executive report (PDF)
└── Project Brief - Customer Lifetime Value & Retention Optimization.pdf
```

The full cleaned dataset and the SQLite database are not included because of file size. To rebuild them, download `online_retail_II.xlsx` from UCI, place it in `Data/`, and run `python src/etl_pipeline.py`, then `python src/generate_minimalist_visualizations.py` and `python src/build_report_and_deck.py`. The Tableau data source expects an ODBC DSN named `Portfolio_DB` pointing to that database.

## Next steps

- Add a simple customer lifetime value estimate per segment
- Compare retention by country (most customers are in the UK)
- Check whether customers whose first order was in Q4 retain differently from those acquired earlier in the year
