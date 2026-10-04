// =============================================================================
// Power Query (M) - paste each block into Home > Transform data > New Source >
// Blank Query > Advanced Editor, then rename the query to the name in the header.
//
// Step 1: create a text parameter named DataFolder
//   (Home > Manage Parameters > New), e.g.
//   C:\Users\<you>\ecommerce-customer-segmentation-cohort-analysis\powerbi\data\
//   The trailing backslash matters.
// =============================================================================

// ---- Query: dim_customer ----------------------------------------------------
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_customer.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"customer_id", Int64.Type}, {"recency_days", Int64.Type}, {"frequency", Int64.Type},
        {"monetary_value", Currency.Type}, {"country", type text}, {"r_score", Int64.Type},
        {"f_score", Int64.Type}, {"m_score", Int64.Type}, {"rfm_score", type text}, {"segment", type text}
    })
in
    Typed

// ---- Query: dim_segment -----------------------------------------------------
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_segment.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"segment", type text}, {"segment_order", Int64.Type}, {"segment_group", type text}, {"recommended_action", type text}
    })
in
    Typed

// ---- Query: fact_cohort -----------------------------------------------------
let
    Source = Csv.Document(File.Contents(DataFolder & "fact_cohort.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"cohort_month", type date}, {"month_index", Int64.Type}, {"activity_month", type date},
        {"cohort_size", Int64.Type}, {"active_customers", Int64.Type}, {"retention_rate", Percentage.Type}
    }, "en-US")
in
    Typed
