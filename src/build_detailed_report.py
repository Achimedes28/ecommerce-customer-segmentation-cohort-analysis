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

BASE_DIR = "/Users/novaldiramadhanwaluyo/Desktop/Certificate and portfolio/Portfolio/Portfolio Data Analyst/E-Commerce Customer Segmentation & Cohort Analysis"
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
            self.drawString(36, 805, "E-Commerce Customer Segmentation & Cohort Analysis | Executive Analytics Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 798, 559, 798)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.drawString(36, 30, "Confidential — Prepared by Novaldi Ramadhan Waluyo (Data Analyst)")
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

    story = []

    # =========================================================================
    # HEADER / TITLE SECTION
    # =========================================================================
    story.append(Paragraph("E-Commerce Customer Segmentation & Cohort Retention Optimization", title_style))
    story.append(Paragraph("Executive Briefing & Strategic Retention Playbook | Addressing +25% CAC Surge", subtitle_style))
    story.append(Paragraph("Author: <b>Novaldi Ramadhan Waluyo</b> (Data Analyst) &nbsp;|&nbsp; Target Audience: <b>CMO, CRM Lead, Product Growth Manager</b>", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BLUE, spaceAfter=10))

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & STRATEGIC CONTEXT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Strategic Business Context", h1_style))
    story.append(Paragraph(
        "Over the past 12 months, the e-commerce retail enterprise recorded a <b>25% surge in Customer Acquisition Costs (CAC)</b>. In response, marketing teams historically relied on aggressive blanket promotions (mass discounting). While this maintained top-of-funnel transaction volume, it attracted short-lived discount seekers, diluted gross profit margins, and triggered massive drop-offs following initial orders.",
        body_style
    ))
    story.append(Paragraph(
        "This data analytics initiative audited <b>1,067,371 raw transaction records</b> spanning a two-year operational window (December 2009 to December 2011). Following rigorous data cleansing, <b>805,549 verified transactions</b> representing <b>5,878 unique registered buyers</b> and <b>£17.74M in gross sales</b> were analyzed using Monthly Cohort Retention tracking and RFM (Recency, Frequency, Monetary) behavioral modeling.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # KPI Scorecard Table
    kpi_table_data = [
        [Paragraph("<b>Analyzed Period</b>", table_cell_bold), Paragraph("<b>Cleaned Transactions</b>", table_cell_bold), Paragraph("<b>Unique Customers</b>", table_cell_bold), Paragraph("<b>Total Gross Revenue</b>", table_cell_bold)],
        [Paragraph("Dec 2009 – Dec 2011 (24 Mo)", table_cell_style), Paragraph("<b>805,549 lines</b> (Filtered from 1.06M)", table_cell_style), Paragraph("<b>5,878 registered buyers</b>", table_cell_style), Paragraph("<b><font color='#2563EB'>£17,743,429.18</font></b>", table_cell_style)],
        [Paragraph("<b>Month-1 Retention Rate</b>", table_cell_bold), Paragraph("<b>Month-1 Churn Drop</b>", table_cell_bold), Paragraph("<b>Champions & Loyalists Share</b>", table_cell_bold), Paragraph("<b>At-Risk Revenue Exposure</b>", table_cell_bold)],
        [Paragraph("<b><font color='#D97706'>25.8% (Avg)</font></b>", table_cell_style), Paragraph("<b><font color='#E11D48'>-74.2% drop-off</font></b>", table_cell_style), Paragraph("<b>62.4% Revenue</b> (28.1% Users)", table_cell_style), Paragraph("<b>£2.68M (15.1% Total)</b>", table_cell_style)]
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
    # SECTION 2: DATA CLEANSING & PIPELINE METHODOLOGY
    # =========================================================================
    story.append(Paragraph("2. Data Cleansing & Pipeline Methodology", h1_style))
    story.append(Paragraph(
        "To ensure analytical integrity and prevent distorted customer lifetime value metrics, the raw data was processed through a standardized Python & SQL pipeline:",
        body_style
    ))
    story.append(Paragraph("• <b>Cancellation Handling:</b> Invoices prefixed with 'C' and negative quantities representing returns/cancellations (~21,000 rows) were isolated.", bullet_style))
    story.append(Paragraph("• <b>Guest Checkout Separation:</b> Records lacking a persistent Customer ID (~240,000 rows) were separated into aggregate baseline tables, retaining strictly registered accounts for longitudinal cohort and RFM tracking.", bullet_style))
    story.append(Paragraph("• <b>Price & Quantity Audits:</b> Erroneous entries (unit prices <= £0.00 or damaged stock adjustments) were removed.", bullet_style))
    story.append(Paragraph("• <b>Temporal & Metric Engineering:</b> Engineered fields include Line Total Sales (Quantity * UnitPrice), Transaction Month, Customer First Purchase Month (Cohort), and Julian Day Recency offsets.", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 3: COHORT RETENTION DEEP DIVE
    # =========================================================================
    story.append(Paragraph("3. Monthly Cohort Retention Analysis (The Month-1 Cliff)", h1_style))
    story.append(Paragraph(
        "Cohort analysis groups customers based on their initial transaction month and tracks their repeat transaction activity across subsequent monthly intervals (Cohort Index 0 to 12+).",
        body_style
    ))
    
    img_cohort = os.path.join(VIZ_DIR, "01_cohort_retention_heatmap.png")
    if os.path.exists(img_cohort):
        story.append(Image(img_cohort, width=7.2*inch, height=3.6*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Key Diagnostic Findings from Cohort Heatmap:", h2_style))
    story.append(Paragraph("1. <b>The Month-1 Cliff (74.2% First-Order Churn):</b> Across all cohorts, customer retention drops drastically from 100% in Month 0 to an average of <b>25.8% in Month 1</b>. Nearly 3 out of 4 new customers never return after their first purchase.", bullet_style))
    story.append(Paragraph("2. <b>Resilient Long-Term Core (20–25% Stabilization):</b> Customers who remain active past Month 3 display strong loyalty, maintaining a steady <b>20% to 25% repeat purchase rate</b> through Month 12 and beyond.", bullet_style))
    story.append(Paragraph("3. <b>Holiday Acquisition Degradation:</b> Customers acquired during Q4 promotional peaks (November 2010) show slightly lower Month-1 retention (~22.1%), confirming that mass holiday discounting attracts non-retaining transactional bargain seekers.", bullet_style))
    story.append(Paragraph("4. <b>Action Window:</b> The primary lifecycle vulnerability occurs in <b>Days 7 to 21 post-purchase</b>. Interventions must engage buyers immediately after order delivery.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: RFM BEHAVIORAL SEGMENTATION
    # =========================================================================
    story.append(Paragraph("4. RFM Customer Segmentation & Monetary Concentration", h1_style))
    story.append(Paragraph(
        "Customers were scored on a 1-to-5 quintile scale across three behavioral dimensions: <b>Recency (R)</b> (days since last purchase), <b>Frequency (F)</b> (count of distinct invoice orders), and <b>Monetary Value (M)</b> (total cumulative spend). Customers were categorized into six actionable operational segments:",
        body_style
    ))
    story.append(Spacer(1, 4))

    # RFM Data Table
    rfm_table_data = [
        [Paragraph("<b>Customer Segment</b>", table_header_style), Paragraph("<b>Count</b>", table_header_style), Paragraph("<b>% Base</b>", table_header_style), Paragraph("<b>Total Revenue (£)</b>", table_header_style), Paragraph("<b>% Rev</b>", table_header_style), Paragraph("<b>Avg Recency</b>", table_header_style), Paragraph("<b>Avg Orders</b>", table_header_style), Paragraph("<b>Avg Spend (£)</b>", table_header_style)],
        [Paragraph("<b>Champions</b>", table_cell_bold), Paragraph("868", table_cell_style), Paragraph("14.8%", table_cell_style), Paragraph("£7,286,211.20", table_cell_style), Paragraph("<b>41.1%</b>", table_cell_bold), Paragraph("12.4 days", table_cell_style), Paragraph("19.8x", table_cell_style), Paragraph("£8,394.25", table_cell_style)],
        [Paragraph("<b>Loyal Customers</b>", table_cell_bold), Paragraph("782", table_cell_style), Paragraph("13.3%", table_cell_style), Paragraph("£3,781,402.15", table_cell_style), Paragraph("<b>21.3%</b>", table_cell_bold), Paragraph("35.6 days", table_cell_style), Paragraph("7.2x", table_cell_style), Paragraph("£4,835.55", table_cell_style)],
        [Paragraph("<b>At Risk</b>", table_cell_bold), Paragraph("945", table_cell_style), Paragraph("16.1%", table_cell_style), Paragraph("£2,684,105.40", table_cell_style), Paragraph("<b>15.1%</b>", table_cell_bold), Paragraph("215.8 days", table_cell_style), Paragraph("4.8x", table_cell_style), Paragraph("£2,840.32", table_cell_style)],
        [Paragraph("<b>Potential Loyalists</b>", table_cell_bold), Paragraph("741", table_cell_style), Paragraph("12.6%", table_cell_style), Paragraph("£1,452,380.90", table_cell_style), Paragraph("8.2%", table_cell_style), Paragraph("48.2 days", table_cell_style), Paragraph("2.9x", table_cell_style), Paragraph("£1,959.95", table_cell_style)],
        [Paragraph("<b>New / Recent</b>", table_cell_bold), Paragraph("982", table_cell_style), Paragraph("16.7%", table_cell_style), Paragraph("£1,120,490.15", table_cell_style), Paragraph("6.3%", table_cell_style), Paragraph("24.1 days", table_cell_style), Paragraph("1.4x", table_cell_style), Paragraph("£1,141.03", table_cell_style)],
        [Paragraph("<b>Hibernating / Lost</b>", table_cell_bold), Paragraph("1,560", table_cell_style), Paragraph("26.5%", table_cell_style), Paragraph("£1,418,839.38", table_cell_style), Paragraph("8.0%", table_cell_style), Paragraph("442.7 days", table_cell_style), Paragraph("1.3x", table_cell_style), Paragraph("£909.51", table_cell_style)]
    ]
    t_rfm = Table(rfm_table_data, colWidths=[92, 38, 42, 95, 45, 65, 55, 75])
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
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ]))
    story.append(t_rfm)
    story.append(Spacer(1, 8))

    img_rfm = os.path.join(VIZ_DIR, "02_rfm_revenue_vs_customers.png")
    if os.path.exists(img_rfm):
        story.append(Image(img_rfm, width=7.2*inch, height=3.4*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Key Segment Inferences:", h2_style))
    story.append(Paragraph("• <b>Extreme Pareto Revenue Concentration:</b> The top two tiers (Champions and Loyal Customers) represent only <b>28.1% of all customers</b> but generate <b>62.4% of total enterprise revenue (£11.06M)</b>.", bullet_style))
    story.append(Paragraph("• <b>High-Value At-Risk Threat:</b> The 'At Risk' segment holds 945 accounts that previously spent an average of £2,840.32 across 4.8 orders, but have been dormant for >200 days. This represents <b>£2.68M in lapsed revenue</b> that requires immediate reactivation.", bullet_style))
    story.append(Paragraph("• <b>High-Volume Dormancy:</b> 26.5% of the database is 'Hibernating' (recency >440 days). Cold paid remarketing to this tier is economically wasteful; low-cost automated email drip campaigns should be used instead.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: MONTHLY REVENUE & ORDER DYNAMICS
    # =========================================================================
    story.append(Paragraph("5. Monthly Revenue Dynamics & Seasonality", h1_style))
    img_growth = os.path.join(VIZ_DIR, "03_monthly_revenue_growth.png")
    if os.path.exists(img_growth):
        story.append(Image(img_growth, width=7.2*inch, height=3.2*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("• <b>Pronounced Q4 Seasonality:</b> Revenue experiences massive holiday surges in October–November (peaking above £1.5M/month). Marketing must deploy automated post-holiday nurture sequences to convert November one-time buyers into Q1 repeat purchasers.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: STAKEHOLDER STRATEGIC PLAYBOOK
    # =========================================================================
    story.append(Paragraph("6. Actionable Strategic Playbook for Key Stakeholders", h1_style))
    story.append(Paragraph(
        "To remediate the 25% CAC surge and capture untapped customer lifetime value, specific tactical initiatives are assigned to core leadership roles:",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("A. Head of Marketing & CMO (Budget & Margin Optimization)", h2_style))
    story.append(Paragraph("1. <b>20% Budget Shift from Acquisition to Retention:</b> Reallocate £200k–£300k from generic broad-match paid search/social ads into automated lifecycle email/SMS infrastructure and customer loyalty programs.", bullet_style))
    story.append(Paragraph("2. <b>Abolish Blanket Public Discounting:</b> Stop sitewide coupon codes that erode product value perception. Restrict financial discounting strictly to high-value At-Risk win-back workflows.", bullet_style))
    story.append(Paragraph("3. <b>Tiered Promo Strategy:</b> Reward Champions with non-monetary VIP perks (early product launches, dedicated concierge, exclusive packaging) rather than price discounts.", bullet_style))
    story.append(Paragraph("4. <b>Projected Impact:</b> Expected 15–20% reduction in blended CAC and +8% expansion in net operating margin.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("B. CRM & Retention Lead (Lifecycle Trigger Automation)", h2_style))
    story.append(Paragraph("1. <b>Automated Day-14 Post-Purchase Onboarding Trigger:</b> Deploy personalized product recommendations based on initial category purchase within 14 days of delivery to bridge the Month-1 cliff.", bullet_style))
    story.append(Paragraph("2. <b>60-Day Inactivity Early Warning Trigger:</b> Automatically trigger re-engagement sequences when a previously active buyer hits 60 days without an order (intervening before they cross into the 200+ day At-Risk churn state).", bullet_style))
    story.append(Paragraph("3. <b>Multi-Channel Routing:</b> Use high-touch WhatsApp/SMS notifications for high-monetary At-Risk customers; use weekly curated newsletters for Loyalists and Potential Loyalists.", bullet_style))
    story.append(Paragraph("4. <b>Dynamic RFM Scoring Pipeline:</b> Automatically recalculate RFM scores weekly to catch segment migrations dynamically.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("C. Product & Growth Manager (User Experience & Telemetry)", h2_style))
    story.append(Paragraph("1. <b>Tiered Loyalty Program:</b> Launch a gamified 4-tier loyalty program (Bronze, Silver, Gold, Platinum) with clear milestones on 3rd and 5th orders to incentivize habit formation.", bullet_style))
    story.append(Paragraph("2. <b>1-Click Frictionless Reordering:</b> Implement quick-reorder buttons on past purchase history pages for consumable, high-frequency SKUs.", bullet_style))
    story.append(Paragraph("3. <b>Live Tableau Telemetry Hub:</b> Maintain real-time tracking of weekly cohort churn and RFM distribution via the automated Tableau ODBC connection.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: TECHNICAL DATA ARCHITECTURE & REPRODUCIBILITY
    # =========================================================================
    story.append(Paragraph("7. Technical Architecture & Implementation Details", h1_style))
    story.append(Paragraph(
        "All analytical models and data assets are structured for complete modularity and automated reproduction:",
        body_style
    ))
    story.append(Paragraph("• <b>SQLite Database (`data/online_retail_analytics.db`):</b> Cleaned line items in `fact_transactions`, RFM scores in `dim_customers_rfm`, cohort tracking in `fact_cohort_activity`, and pre-aggregated analytical views.", bullet_style))
    story.append(Paragraph("• <b>Automated Tableau ODBC Connector (`tableau/online_retail_analytics.tds`):</b> Pre-configured Data Source XML enabling instant live connection in Tableau Desktop with zero manual schema setup.", bullet_style))
    story.append(Paragraph("• <b>Production SQL Scripts (`/sql/`):</b> Dedicated scripts for schema DDL (`01_schema_and_views.sql`), cohort queries (`02_cohort_analysis.sql`), and RFM scoring (`03_rfm_segmentation.sql`).", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Comprehensive Multi-Page PDF Report generated successfully: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_pdf_report()
