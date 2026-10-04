#!/usr/bin/env python3
"""
Comprehensive Executive & Technical Analytics Report (Multi-Page PDF)
Domain: E-Commerce & Retail Operations Analytics
"""

import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from report_metrics import load_metrics, money, money_m, pct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")
os.makedirs(REPORT_DIR, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 805, "E-Commerce Customer Segmentation & Cohort Retention | Executive Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 798, 559, 798)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.drawString(36, 30, "Prepared by Novaldi Ramadhan Waluyo (Data Analyst)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 30, page_str)
        self.restoreState()

def generate_pdf_report():
    pdf_path = os.path.join(REPORT_DIR, "Executive_Report_Customer_Segmentation_Cohort.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette Styles
    C_NAVY = colors.HexColor("#0F172A")
    C_BLUE = colors.HexColor("#2563EB")
    C_MUTED = colors.HexColor("#475569")
    C_LIGHT_BG = colors.HexColor("#F8FAFC")
    C_BORDER = colors.HexColor("#CBD5E1")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=C_NAVY,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=C_MUTED,
        spaceAfter=10
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=C_BLUE,
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=C_NAVY,
        spaceBefore=14,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_BLUE,
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=14,
        spaceAfter=3
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    m = load_metrics()
    seg = m["seg"]
    cm1 = m["cohort_m1"]

    def bullet(text):
        story.append(Paragraph(f"• {text}", bullet_style))

    story = []

    # =========================================================================
    # HEADER / TITLE SECTION
    # =========================================================================
    story.append(Paragraph("E-Commerce Customer Segmentation & Cohort Retention", title_style))
    story.append(Paragraph("Executive briefing and retention playbook", subtitle_style))
    story.append(Paragraph("Author: <b>Novaldi Ramadhan Waluyo</b> (Data Analyst) &nbsp;|&nbsp; Audience: <b>CMO, CRM Lead, Product & Growth Manager</b>", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BLUE, spaceAfter=10))

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "The project brief describes a <b>25% rise in Customer Acquisition Cost (CAC)</b> over 12 months while marketing still relies on "
        "untargeted mass promotions. The question is where customers drop off after their first order and which customers are worth investing in.",
        body_style
    ))
    story.append(Paragraph(
        f"The analysis covers <b>{m['raw_rows']:,} raw transaction lines</b> from {m['period']}. After cleaning, "
        f"<b>{m['clean_rows']:,} lines</b> from <b>{m['customers']:,} registered customers</b> in {m['countries']} countries "
        f"(<b>{money_m(m['revenue'])}</b> revenue, {m['orders']:,} orders) were analysed with monthly cohort retention and RFM segmentation.",
        body_style
    ))
    story.append(Spacer(1, 4))

    kpi_table_data = [
        [Paragraph("<b>Period</b>", table_cell_bold), Paragraph("<b>Cleaned lines</b>", table_cell_bold), Paragraph("<b>Customers</b>", table_cell_bold), Paragraph("<b>Revenue</b>", table_cell_bold)],
        [Paragraph(m["period"], table_cell_style), Paragraph(f"{m['clean_rows']:,} (from {m['raw_rows'] / 1e6:.2f}M)", table_cell_style), Paragraph(f"{m['customers']:,} in {m['countries']} countries", table_cell_style), Paragraph(f"<b><font color='#2563EB'>{money(m['revenue'], 2)}</font></b>", table_cell_style)],
        [Paragraph("<b>Month-1 retention</b>", table_cell_bold), Paragraph("<b>Not back in month 1</b>", table_cell_bold), Paragraph("<b>Champions + Loyal</b>", table_cell_bold), Paragraph("<b>At Risk revenue</b>", table_cell_bold)],
        [Paragraph(f"<b>{pct(m['m1'])}</b> (customer-weighted)", table_cell_style), Paragraph(f"<b>{pct(m['m1_churn'])}</b> of new customers", table_cell_style), Paragraph(f"<b>{pct(m['core_pct_revenue'])}</b> of revenue from {pct(m['core_pct_customers'])} of customers", table_cell_style), Paragraph(f"<b>{money_m(seg.loc['At Risk', 'revenue'])}</b> ({pct(seg.loc['At Risk', 'pct_revenue'])} of total)", table_cell_style)]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[130, 130, 130, 133])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: DATA PREPARATION
    # =========================================================================
    story.append(Paragraph("2. Data Preparation", h1_style))
    story.append(Paragraph("The raw Online Retail II workbook (two yearly sheets) was processed in Python (<font face='Courier'>src/etl_pipeline.py</font>) and loaded into SQLite:", body_style))
    bullet("<b>Cancellations and returns:</b> invoices starting with 'C' and lines with quantity &lt;= 0 were removed.")
    bullet("<b>Guest checkouts:</b> lines without a Customer ID were excluded, because cohort and RFM analysis need a persistent customer.")
    bullet("<b>Invalid prices:</b> lines with a unit price &lt;= £0 were removed.")
    bullet("<b>Engineered fields:</b> line revenue (quantity × unit price), invoice month, cohort month (first purchase) and recency in days from 10 Dec 2011.")
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 3: COHORT RETENTION
    # =========================================================================
    cohort_block = [
        Paragraph("3. Monthly Cohort Retention", h1_style),
        Paragraph("Customers are grouped by the month of their first purchase and tracked by how many buy again in each following month (month 0 to 24).", body_style),
    ]
    img_cohort = os.path.join(VIZ_DIR, "01_cohort_retention_heatmap.png")
    if os.path.exists(img_cohort):
        cohort_block += [Image(img_cohort, width=7.2*inch, height=3.6*inch), Spacer(1, 6)]
    story.append(KeepTogether(cohort_block))

    holiday = ", ".join(f"{d:%b %Y} {pct(cm1[d])}" for d in pd.to_datetime(["2010-11-01", "2010-12-01"]))
    story.append(Paragraph("Findings", h2_style))
    bullet(f"<b>The month-1 cliff:</b> only <b>{pct(m['m1'])}</b> of new customers buy again in the month after their first order, so {pct(m['m1_churn'])} do not come back that month.")
    bullet(f"<b>Flat after the cliff:</b> retention stays between <b>{pct(m['retention_min_m1_m12'])} and {pct(m['retention_max_m1_m12'])}</b> from month 1 to month 12. The second purchase is the main lever.")
    bullet(f"<b>Holiday cohorts retain worst:</b> month-1 retention for customers acquired in the Q4 peak was {holiday}, against the {pct(m['m1'])} average, consistent with promotions attracting one-off buyers.")
    bullet("<b>Action window:</b> follow-up has to happen within the first 30 days, before the next month starts.")
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: RFM SEGMENTATION
    # =========================================================================
    story.append(Paragraph("4. RFM Segmentation", h1_style))
    story.append(Paragraph(
        "Each customer is scored 1 to 5 (quintiles) on <b>Recency</b> (days since last order), <b>Frequency</b> (distinct orders) and "
        "<b>Monetary value</b> (total spend), then assigned to one of seven segments.",
        body_style
    ))
    story.append(Spacer(1, 4))

    header = ["Segment", "Customers", "% base", "Revenue", "% rev", "Avg recency", "Avg orders", "Avg spend"]
    rfm_table_data = [[Paragraph(f"<b>{h}</b>", table_header_style) for h in header]]
    for name, r in seg.iterrows():
        rfm_table_data.append([
            Paragraph(f"<b>{name}</b>", table_cell_bold),
            Paragraph(f"{int(r.customers):,}", table_cell_style),
            Paragraph(pct(r.pct_customers), table_cell_style),
            Paragraph(money(r.revenue), table_cell_style),
            Paragraph(f"<b>{pct(r.pct_revenue)}</b>", table_cell_bold),
            Paragraph(f"{r.recency:.0f} days", table_cell_style),
            Paragraph(f"{r.orders:.1f}", table_cell_style),
            Paragraph(money(r.spend), table_cell_style),
        ])
    t_rfm = Table(rfm_table_data, colWidths=[100, 50, 42, 78, 42, 62, 52, 62])
    t_rfm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rfm)
    story.append(Spacer(1, 8))

    img_rfm = os.path.join(VIZ_DIR, "02_rfm_revenue_vs_customers.png")
    if os.path.exists(img_rfm):
        story.append(Image(img_rfm, width=7.2*inch, height=3.7*inch))
        story.append(Spacer(1, 6))

    champ, risk = seg.loc["Champions"], seg.loc["At Risk"]
    story.append(Paragraph("Findings", h2_style))
    bullet(f"<b>Revenue is concentrated:</b> Champions are {pct(champ.pct_customers)} of customers but {pct(champ.pct_revenue)} of revenue. "
           f"With Loyal Customers, the top two segments ({m['core_customers']:,} customers, {pct(m['core_pct_customers'])}) bring in {pct(m['core_pct_revenue'])} ({money_m(m['core_revenue'])}).")
    bullet(f"<b>High-value customers at risk:</b> {int(risk.customers):,} At Risk customers averaged {risk.orders:.1f} orders and {money(risk.spend)} spend, "
           f"but last ordered about {risk.recency:.0f} days ago on average. Together they represent <b>{money_m(risk.revenue)}</b> of historical revenue worth winning back.")
    bullet(f"<b>Large dormant tail:</b> Hibernating and Lost customers are {pct(m['dormant_pct_customers'])} of the base but only {pct(m['dormant_pct_revenue'])} of revenue. "
           "Paid remarketing to them is unlikely to pay back; low-cost email is enough.")
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: MONTHLY REVENUE
    # =========================================================================
    revenue_block = [Paragraph("5. Monthly Revenue and Seasonality", h1_style)]
    img_growth = os.path.join(VIZ_DIR, "03_monthly_revenue_growth.png")
    if os.path.exists(img_growth):
        revenue_block += [Image(img_growth, width=7.2*inch, height=3.7*inch), Spacer(1, 6)]
    story.append(KeepTogether(revenue_block))

    bullet("<b>Strong Q4 seasonality:</b> revenue climbs from September and peaks in November in both years at around £1.2M a month, roughly twice the Q1 level.")
    bullet("<b>December 2011 is partial:</b> the data ends on 9 December 2011, so the final drop is not a real decline.")
    bullet("<b>Implication:</b> Q4 has the most active customers but the holiday cohorts retain worst, so a January re-engagement flow for November and December first-time buyers matters most.")

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: PLAYBOOK
    # =========================================================================
    story.append(Paragraph("6. Retention Playbook", h1_style))
    story.append(Paragraph("Recommended actions by owner. Each should be run as a controlled test (holdout group) before full rollout.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("A. Head of Marketing / CMO: budget and margin", h2_style))
    story.append(Paragraph("1. <b>Shift budget from acquisition to retention:</b> move part of the broad paid-media budget into lifecycle email/SMS for New and At Risk customers.", bullet_style))
    story.append(Paragraph("2. <b>Stop blanket discounts:</b> keep discounts for targeted At Risk win-back offers only.", bullet_style))
    story.append(Paragraph("3. <b>Reward Champions without margin:</b> early access, exclusive products and service perks instead of price cuts.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("B. CRM & Retention Lead: lifecycle triggers", h2_style))
    story.append(Paragraph("1. <b>14-day post-purchase flow:</b> personalised recommendations based on the first order's category, to close the month-1 gap.", bullet_style))
    story.append(Paragraph(f"2. <b>60-day inactivity trigger:</b> start re-engagement when a customer passes 60 days without an order, well before the At Risk level (~{risk.recency:.0f} days on average).", bullet_style))
    story.append(Paragraph("3. <b>Channel by value:</b> SMS/WhatsApp for high-value At Risk customers, a regular newsletter for Loyal and Potential Loyalists.", bullet_style))
    story.append(Paragraph("4. <b>Refresh RFM scores weekly</b> so customers moving between segments are caught early.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("C. Product & Growth Manager: habit and tracking", h2_style))
    story.append(Paragraph("1. <b>Loyalty tiers</b> with milestones at the 3rd and 5th order to move Potential Loyalists up.", bullet_style))
    story.append(Paragraph("2. <b>One-click reorder</b> from order history for frequently repurchased items.", bullet_style))
    story.append(Paragraph("3. <b>Track retention in the Power BI dashboard</b> (Overview, Cohort Retention, RFM Segments) to monitor month-1 retention and segment shifts.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: TECHNICAL ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("7. Technical Architecture", h1_style))
    bullet("<b>SQLite database</b> (<font face='Courier'>data/online_retail_analytics.db</font>, built by the ETL script): <font face='Courier'>fact_transactions</font>, <font face='Courier'>dim_customers_rfm</font>, <font face='Courier'>fact_cohort_activity</font> and analytical views.")
    bullet("<b>SQL</b> (<font face='Courier'>sql/</font>): schema and views, cohort retention query, RFM scoring with <font face='Courier'>NTILE(5)</font>.")
    bullet("<b>Power BI</b> (<font face='Courier'>powerbi/</font>): star-schema tables, DAX measures, theme and build guide for a three-page dashboard.")
    bullet("<b>Tableau</b> (<font face='Courier'>tableau/online_retail_analytics.tds</font>): data source for a live SQLite connection via ODBC.")
    bullet("<b>Report figures</b> are computed in <font face='Courier'>src/report_metrics.py</font>, so the README, this report and the slide deck stay in sync.")
    story.append(Spacer(1, 8))

    story.append(Paragraph("Notes and limitations", h2_style))
    bullet(f"The December 2009 cohort includes customers who bought before the data starts, which inflates its retention ({pct(cm1.iloc[0])} in month 1).")
    bullet("Customer-weighted retention divides all returning customers by all cohort customers that reached that month, so large cohorts weigh more.")
    bullet("Recommendations are hypotheses to test; the data does not include marketing spend, so CAC impact cannot be measured here.")

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Comprehensive Multi-Page PDF Report generated successfully: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_pdf_report()
