-- =============================================================================
-- RFM (RECENCY, FREQUENCY, MONETARY) SEGMENTATION (SQL IMPLEMENTATION)
-- Reference Date: Dataset Max Date + 1 Day (2011-12-10)
-- =============================================================================

WITH raw_rfm AS (
    SELECT 
        customer_id,
        CAST((JULIANDAY('2011-12-10') - JULIANDAY(MAX(invoice_date_str))) AS INTEGER) AS recency_days,
        COUNT(DISTINCT invoice_no) AS frequency,
        ROUND(SUM(total_sales), 2) AS monetary_value,
        MAX(country) AS country
    FROM fact_transactions
    GROUP BY customer_id
),

rfm_scoring AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary_value,
        country,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM raw_rfm
)

SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    country,
    r_score,
    f_score,
    m_score,
    (CAST(r_score AS TEXT) || CAST(f_score AS TEXT) || CAST(m_score AS TEXT)) AS rfm_score,
    CASE 
        WHEN r_score >= 4 AND (f_score + m_score)/2.0 >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND (f_score + m_score)/2.0 >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND (f_score + m_score)/2.0 <= 2 THEN 'New / Recent Customers'
        WHEN r_score >= 3 AND (f_score + m_score)/2.0 <= 3 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND (f_score + m_score)/2.0 >= 3 THEN 'At Risk'
        WHEN r_score = 1 AND (f_score + m_score)/2.0 >= 4 THEN 'Cannot Lose Them'
        WHEN r_score <= 2 AND (f_score + m_score)/2.0 <= 2 THEN 'Hibernating'
        ELSE 'Lost / Others'
    END AS segment
FROM rfm_scoring;
