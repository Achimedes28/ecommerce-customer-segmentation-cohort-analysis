-- =============================================================================
-- PORTFOLIO CASE STUDY: E-COMMERCE CUSTOMER SEGMENTATION & COHORT RETENTION
-- Database: SQLite (online_retail_analytics.db)
-- Domain: Retail & E-Commerce Operations Analytics
-- =============================================================================

-- 1. FACT TRANSACTIONS TABLE SCHEMA
CREATE TABLE IF NOT EXISTS fact_transactions (
    invoice_no TEXT,
    stock_code TEXT,
    description TEXT,
    quantity INTEGER,
    invoice_date_str TEXT,
    unit_price REAL,
    total_sales REAL,
    customer_id INTEGER,
    country TEXT
);

-- 2. DIMENSION CUSTOMERS RFM TABLE SCHEMA
CREATE TABLE IF NOT EXISTS dim_customers_rfm (
    customer_id INTEGER PRIMARY KEY,
    recency_days INTEGER,
    frequency INTEGER,
    monetary_value REAL,
    country TEXT,
    r_score INTEGER,
    f_score INTEGER,
    m_score INTEGER,
    rfm_score TEXT,
    segment TEXT
);

-- 3. COHORT ACTIVITY TABLE SCHEMA
CREATE TABLE IF NOT EXISTS fact_cohort_activity (
    cohort_month TEXT,
    cohort_index INTEGER,
    customer_id INTEGER
);

-- 4. PERFORMANCE INDEXES
CREATE INDEX IF NOT EXISTS idx_trans_cust ON fact_transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_trans_date ON fact_transactions(invoice_date_str);
CREATE INDEX IF NOT EXISTS idx_trans_country ON fact_transactions(country);
CREATE INDEX IF NOT EXISTS idx_rfm_cust ON dim_customers_rfm(customer_id);
CREATE INDEX IF NOT EXISTS idx_rfm_seg ON dim_customers_rfm(segment);

-- 5. ANALYTICAL VIEW: RFM SEGMENT PERFORMANCE SCORECARD
CREATE VIEW IF NOT EXISTS v_rfm_summary AS
SELECT 
    segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM dim_customers_rfm), 2) AS pct_customers,
    ROUND(SUM(monetary_value), 2) AS total_revenue,
    ROUND(SUM(monetary_value) * 100.0 / (SELECT SUM(monetary_value) FROM dim_customers_rfm), 2) AS pct_revenue,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency_orders,
    ROUND(AVG(monetary_value), 2) AS avg_monetary_spend
FROM dim_customers_rfm
GROUP BY segment
ORDER BY total_revenue DESC;

-- 6. ANALYTICAL VIEW: MONTHLY REVENUE & ORDER DYNAMICS
CREATE VIEW IF NOT EXISTS v_monthly_sales_trend AS
SELECT 
    SUBSTR(invoice_date_str, 1, 7) AS year_month,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND(SUM(total_sales), 2) AS total_revenue,
    ROUND(SUM(total_sales) / COUNT(DISTINCT invoice_no), 2) AS avg_order_value
FROM fact_transactions
GROUP BY SUBSTR(invoice_date_str, 1, 7)
ORDER BY year_month ASC;

-- 7. ANALYTICAL VIEW: TOP PRODUCT VOLUME & REVENUE (PARETO)
CREATE VIEW IF NOT EXISTS v_top_products AS
SELECT 
    stock_code,
    description,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(total_sales), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS order_occurrences
FROM fact_transactions
GROUP BY stock_code, description
ORDER BY total_revenue DESC
LIMIT 50;
