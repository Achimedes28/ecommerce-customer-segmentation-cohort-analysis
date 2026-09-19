-- =============================================================================
-- COHORT RETENTION ANALYSIS (SQL IMPLEMENTATION)
-- Objective: Map customer retention rate across 0-12+ months from acquisition
-- =============================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        MIN(SUBSTR(invoice_date_str, 1, 7)) AS cohort_month
    FROM fact_transactions
    GROUP BY customer_id
),

cohort_activity AS (
    SELECT 
        t.customer_id,
        c.cohort_month,
        SUBSTR(t.invoice_date_str, 1, 7) AS activity_month,
        (
            (CAST(SUBSTR(t.invoice_date_str, 1, 4) AS INTEGER) - CAST(SUBSTR(c.cohort_month, 1, 4) AS INTEGER)) * 12 +
            (CAST(SUBSTR(t.invoice_date_str, 6, 2) AS INTEGER) - CAST(SUBSTR(c.cohort_month, 6, 2) AS INTEGER))
        ) AS cohort_index
    FROM fact_transactions t
    JOIN customer_first_purchase c ON t.customer_id = c.customer_id
),

cohort_summary AS (
    SELECT 
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohort_activity
    GROUP BY cohort_month, cohort_index
),

cohort_initial_size AS (
    SELECT 
        cohort_month,
        active_customers AS initial_cohort_size
    FROM cohort_summary
    WHERE cohort_index = 0
)

SELECT 
    s.cohort_month,
    i.initial_cohort_size,
    s.cohort_index,
    s.active_customers,
    ROUND((s.active_customers * 100.0 / i.initial_cohort_size), 2) AS retention_rate_pct
FROM cohort_summary s
JOIN cohort_initial_size i ON s.cohort_month = i.cohort_month
ORDER BY s.cohort_month, s.cohort_index;
