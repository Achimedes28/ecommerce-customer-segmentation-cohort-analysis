#!/usr/bin/env python3
"""
Professional Executive Slide Deck Generator (16:9 Widescreen)
Optimized typography, tight spacing, zero dead space, modern dark-slate UI aesthetic.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = "/Users/novaldiramadhanwaluyo/Desktop/Certificate and portfolio/Portfolio/Portfolio Data Analyst/E-Commerce Customer Segmentation & Cohort Analysis"
PRES_DIR = os.path.join(BASE_DIR, "presentations")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(PRES_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# DESIGN SYSTEM & COLOR PALETTE
# -----------------------------------------------------------------------------
C_BG = RGBColor(11, 15, 25)         # Deep Obsidian Canvas #0B0F19
C_CARD = RGBColor(19, 27, 46)       # Surface Navy Card #131B2E
C_CARD_ALT = RGBColor(26, 36, 61)   # Elevated Card #1A243D
C_BORDER = RGBColor(38, 52, 84)     # Crisp Border #263454
C_BORDER_SUBTLE = RGBColor(28, 39, 64)

C_WHITE = RGBColor(248, 250, 252)   # Title / High Emphasis #F8FAFC
C_TEXT = RGBColor(226, 232, 240)    # Body #E2E8F0
C_MUTED = RGBColor(148, 163, 184)   # Secondary / Labels #94A3B8
C_DIM = RGBColor(100, 116, 139)     # Micro Metadata #64748B

C_CYAN = RGBColor(56, 189, 248)     # Primary Accent (Sky Blue) #38BDF8
C_INDIGO = RGBColor(129, 140, 248)  # Secondary Accent #818CF8
C_AMBER = RGBColor(245, 158, 11)    # Risk / Warning #F59E0B
C_EMERALD = RGBColor(16, 185, 129)  # Growth / Positive #10B981
C_ROSE = RGBColor(244, 63, 94)      # Critical Alert #F43F5E

def set_card_style(shape, bg_color=C_CARD, border_color=C_BORDER):
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()

def add_header(slide, title_text, kicker="EXECUTIVE DATA ANALYTICS CASE STUDY"):
    # Category Kicker Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(3.8), Inches(0.32))
    set_card_style(pill, bg_color=C_CARD_ALT, border_color=C_BORDER)
    ptf = pill.text_frame
    ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    ptf.margin_left = ptf.margin_right = ptf.margin_top = ptf.margin_bottom = 0
    p = ptf.paragraphs[0]
    p.text = kicker.upper()
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER
    
    # Main Slide Title
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.7), Inches(0.55))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p2 = tf.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_canvas(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        set_card_style(bg, bg_color=C_BG, border_color=None)
        return bg

    # =========================================================================
    # SLIDE 1: HERO / COVER (High-Impact Title + Executive Summary + Stat Pills)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_canvas(s1)

    # Hero Main Card Container
    hero_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    set_card_style(hero_card, bg_color=C_CARD, border_color=C_BORDER)
    
    # Title Block Textbox
    tb_title = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(3.2))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    
    p_kicker = tf1.paragraphs[0]
    p_kicker.text = "RETAIL & E-COMMERCE ANALYTICS | EXECUTIVE DELIVERABLE"
    p_kicker.font.size = Pt(11)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = C_CYAN
    p_kicker.space_after = Pt(10)
    
    p_main = tf1.add_paragraph()
    p_main.text = "Customer Segmentation & Cohort Retention Optimization"
    p_main.font.size = Pt(30)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(10)
    
    p_sub = tf1.add_paragraph()
    p_sub.text = "Overcoming a 25% Surge in Customer Acquisition Costs via Behavioral RFM Modeling, Month-1 Churn Analysis, and Precision Lifecycle Marketing."
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = C_MUTED
    p_sub.space_after = Pt(20)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Author: Novaldi Ramadhan Waluyo (Data Analyst)   •   Target Stakeholders: CMO, CRM Lead, Product Growth Manager"
    p_meta.font.size = Pt(10.5)
    p_meta.font.color.rgb = C_AMBER

    # 4 Quick Stat Pills inside Hero
    stats = [
        ("TOTAL REVENUE", "£17.74M", C_EMERALD),
        ("VALID TRANSACTIONS", "805.5K", C_CYAN),
        ("UNIQUE CUSTOMERS", "5,878", C_INDIGO),
        ("MONTH-1 CHURN DROP", "-74.2%", C_ROSE)
    ]
    pill_w = Inches(2.55)
    pill_h = Inches(1.1)
    pill_y = Inches(5.1)
    for i, (st_lbl, st_val, st_col) in enumerate(stats):
        px = Inches(1.3 + i * 2.7)
        sp = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, pill_y, pill_w, pill_h)
        set_card_style(sp, bg_color=C_CARD_ALT, border_color=C_BORDER)
        sptf = sp.text_frame
        sptf.vertical_anchor = MSO_ANCHOR.MIDDLE
        sptf.margin_left = sptf.margin_right = sptf.margin_top = sptf.margin_bottom = 0
        
        p1 = sptf.paragraphs[0]
        p1.text = st_lbl
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_MUTED
        p1.alignment = PP_ALIGN.CENTER
        
        p2 = sptf.add_paragraph()
        p2.text = st_val
        p2.font.size = Pt(19)
        p2.font.bold = True
        p2.font.color.rgb = st_col
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: EXECUTIVE SCORECARD & PROBLEM STATEMENT (No dead space)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_canvas(s2)
    add_header(s2, "Executive Scorecard & Strategic Problem Statement")

    # 4 Top KPI Cards
    top_kpis = [
        ("TOTAL MONETARY VALUE", "£17.74M", "Net valid revenue across 2 years", C_EMERALD),
        ("CUSTOMER BASE", "5,878", "Analyzed registered purchasers", C_CYAN),
        ("MONTH-1 RETENTION", "25.8%", "Drop-off occurs in first 30-60 days", C_AMBER),
        ("TOP REVENUE SHARE", "62.4%", "Driven by top 28.1% Champions & Loyalists", C_INDIGO)
    ]
    kw = Inches(2.78)
    kh = Inches(1.25)
    ky = Inches(1.4)
    for i, (title, val, sub, col) in enumerate(top_kpis):
        kx = Inches(0.8 + i * 2.98)
        kcard = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kx, ky, kw, kh)
        set_card_style(kcard, bg_color=C_CARD, border_color=C_BORDER)
        ktf = kcard.text_frame
        ktf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ktf.margin_left = Inches(0.15)
        ktf.margin_right = Inches(0.15)
        ktf.margin_top = ktf.margin_bottom = 0
        
        p1 = ktf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = C_MUTED
        
        p2 = ktf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_before = Pt(2)
        
        p3 = ktf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(7.5)
        p3.font.color.rgb = C_DIM
        p3.space_before = Pt(2)

    # 2 Big Structured Analytical Panels Below
    panel_y = Inches(2.85)
    panel_h = Inches(4.15)
    panel_w = Inches(5.72)

    # Left Panel: Root Causes & Vulnerabilities
    lp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), panel_y, panel_w, panel_h)
    set_card_style(lp, bg_color=C_CARD, border_color=C_BORDER)
    lptf = lp.text_frame
    lptf.word_wrap = True
    lptf.margin_left = lptf.margin_right = Inches(0.25)
    lptf.margin_top = Inches(0.2)
    lptf.margin_bottom = Inches(0.15)
    
    p = lptf.paragraphs[0]
    p.text = "CORE VULNERABILITIES & PROBLEM ROOT CAUSE"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p.space_after = Pt(8)

    vulns = [
        ("CAC Inflation (+25% YoY):", "Rapid escalation in paid advertising costs makes one-and-done buyers economically unviable."),
        ("Inefficient Mass Discounting:", "Blanket promotions eroded gross profit margins while attracting price-sensitive bargain hunters with high churn rates."),
        ("The First-Order Drop-off Cliff:", "74.2% of newly acquired customers never make a second purchase, collapsing lifecycle customer value."),
        ("Unstructured CRM Engagement:", "Absence of automated behavioral triggers allowed high-spend customers to silently lapse into the 'At Risk' category.")
    ]
    for vt, vd in vulns:
        p_t = lptf.add_paragraph()
        p_t.text = f"• {vt} "
        p_t.font.bold = True
        p_t.font.size = Pt(9.5)
        p_t.font.color.rgb = C_WHITE
        p_t.space_before = Pt(6)
        
        p_d = lptf.add_paragraph()
        p_d.text = f"  {vd}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = C_MUTED
        p_d.space_before = Pt(1)

    # Right Panel: Strategic Objectives & Quantified Goals
    rp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.81), panel_y, panel_w, panel_h)
    set_card_style(rp, bg_color=C_CARD, border_color=C_BORDER)
    rptf = rp.text_frame
    rptf.word_wrap = True
    rptf.margin_left = rptf.margin_right = Inches(0.25)
    rptf.margin_top = Inches(0.2)
    rptf.margin_bottom = Inches(0.15)

    p = rptf.paragraphs[0]
    p.text = "STRATEGIC OBJECTIVES & REMEDIATION GOALS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(8)

    goals = [
        ("Shift Budget to Retention (20% Reallocation):", "Move budget away from low-intent cold ads toward automated post-purchase onboarding sequences."),
        ("Targeted RFM Margin Protection:", "Stop discounting Champions (offer VIP perks); focus financial discounts exclusively on high-value At-Risk win-backs."),
        ("Bridge the Month-1 Window (Days 7-21):", "Deploy personalized cross-sell triggers within 14 days of purchase to lift Month-1 retention from 25.8% to >35%."),
        ("Live Tableau Retention Telemetry:", "Automate ODBC pipeline to track weekly cohort health and RFM migrations in real time.")
    ]
    for gt, gd in goals:
        p_t = rptf.add_paragraph()
        p_t.text = f"• {gt} "
        p_t.font.bold = True
        p_t.font.size = Pt(9.5)
        p_t.font.color.rgb = C_WHITE
        p_t.space_before = Pt(6)
        
        p_d = rptf.add_paragraph()
        p_d.text = f"  {gd}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = C_MUTED
        p_d.space_before = Pt(1)

    # =========================================================================
    # SLIDE 3: COHORT RETENTION DEEP DIVE (Heatmap + 3 Snug Cards)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_canvas(s3)
    add_header(s3, "Cohort Retention Analysis: Mapping the Month-1 Churn Cliff")

    # Left Container: Chart Frame
    chart_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.6))
    set_card_style(chart_card, bg_color=C_CARD, border_color=C_BORDER)
    
    img_cohort = os.path.join(VIZ_DIR, "01_cohort_retention_heatmap.png")
    if os.path.exists(img_cohort):
        s3.shapes.add_picture(img_cohort, Inches(0.95), Inches(1.55), width=Inches(7.1))

    # Right Container: 3 Structured Vertical Insight Cards (Fills entire 5.6" height)
    rc_w = Inches(4.13)
    rc_h = Inches(1.76)
    rc_x = Inches(8.4)
    
    r_insights = [
        ("THE MONTH-1 CLIFF (-74.2% DROP)", 
         "Average retention collapses from 100% to 25.8% in Month 1. Over 7 out of 10 buyers never make a repeat purchase without active intervention.",
         C_ROSE),
        ("LONG-TERM STABILIZATION (20-25%)", 
         "Customers retained past Month 3 form a resilient core, sustaining 20-25% repeat activity through Month 12+. Early retention compounds lifetime value.",
         C_CYAN),
        ("ACTION WINDOW: DAYS 7 TO 21", 
         "Automated follow-ups must fire within 14 days of order delivery while product enthusiasm is high, before customer purchase intent cools down completely.",
         C_AMBER)
    ]
    for i, (title, body, col) in enumerate(r_insights):
        ry = Inches(1.4 + i * 1.92)
        icard = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_x, ry, rc_w, rc_h)
        set_card_style(icard, bg_color=C_CARD, border_color=C_BORDER)
        ictf = icard.text_frame
        ictf.word_wrap = True
        ictf.margin_left = ictf.margin_right = Inches(0.2)
        ictf.margin_top = Inches(0.15)
        ictf.margin_bottom = Inches(0.1)
        
        p1 = ictf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(4)
        
        p2 = ictf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = C_TEXT
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: RFM SEGMENTATION MATRIX (Pareto + Value Distribution)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_canvas(s4)
    add_header(s4, "RFM Behavioral Segmentation: Revenue Concentration & Tiers")

    # Left Container: Chart Frame
    rfm_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.6))
    set_card_style(rfm_card, bg_color=C_CARD, border_color=C_BORDER)
    
    img_rfm = os.path.join(VIZ_DIR, "02_rfm_revenue_vs_customers.png")
    if os.path.exists(img_rfm):
        s4.shapes.add_picture(img_rfm, Inches(0.95), Inches(1.55), width=Inches(7.1))

    # Right Container: 3 Actionable Tier Cards
    r_tiers = [
        ("CHAMPIONS (41.1% REVENUE | 14.8% USERS)", 
         "868 VIPs generate £7.28M with 19.8 avg orders (£8.39k spend). Strategy: Dedicated VIP support, product co-creation, zero discounting.",
         C_EMERALD),
        ("LOYAL & POTENTIAL (29.5% REVENUE)", 
         "1,523 steady buyers contributing £5.23M. Strategy: Milestone loyalty tiers, cross-category recommendations, threshold spend bonuses.",
         C_CYAN),
        ("AT RISK & CAN'T LOSE (15.1% REVENUE)", 
         "945 high-spend customers inactive >200 days (£2.68M revenue at stake). Strategy: Aggressive automated win-back emails & reactivation discounts.",
         C_AMBER)
    ]
    for i, (title, body, col) in enumerate(r_tiers):
        ry = Inches(1.4 + i * 1.92)
        icard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_x, ry, rc_w, rc_h)
        set_card_style(icard, bg_color=C_CARD, border_color=C_BORDER)
        ictf = icard.text_frame
        ictf.word_wrap = True
        ictf.margin_left = ictf.margin_right = Inches(0.2)
        ictf.margin_top = Inches(0.15)
        ictf.margin_bottom = Inches(0.1)
        
        p1 = ictf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(4)
        
        p2 = ictf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = C_TEXT
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: REVENUE TRENDS & SEASONALITY (Full Height Optimization)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_canvas(s5)
    add_header(s5, "Monthly Revenue & Order Dynamics (2009 - 2011)")

    # Chart on Left
    rev_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.6))
    set_card_style(rev_card, bg_color=C_CARD, border_color=C_BORDER)
    
    img_growth = os.path.join(VIZ_DIR, "03_monthly_revenue_growth.png")
    if os.path.exists(img_growth):
        s5.shapes.add_picture(img_growth, Inches(0.95), Inches(1.55), width=Inches(7.1))

    # Right 3 Temporal Cards
    r_season = [
        ("Q4 HOLIDAY SURGE (>£1.5M/MO)", 
         "Massive seasonal peak occurring consistently in October-November. Retail demand increases order volume by +140% vs Q1 baseline.",
         C_EMERALD),
        ("POST-HOLIDAY CHURN MANAGEMENT", 
         "Massive buyer inflow in November requires structured January reactivation sequences to prevent immediate transition to Hibernating state.",
         C_CYAN),
        ("ORDER BASKET SIZING", 
         "Average Order Value (AOV) peaks alongside seasonal gifting SKUs. Cross-sell bundles during checkout maximize basket monetization.",
         C_INDIGO)
    ]
    for i, (title, body, col) in enumerate(r_season):
        ry = Inches(1.4 + i * 1.92)
        icard = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_x, ry, rc_w, rc_h)
        set_card_style(icard, bg_color=C_CARD, border_color=C_BORDER)
        ictf = icard.text_frame
        ictf.word_wrap = True
        ictf.margin_left = ictf.margin_right = Inches(0.2)
        ictf.margin_top = Inches(0.15)
        ictf.margin_bottom = Inches(0.1)
        
        p1 = ictf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(4)
        
        p2 = ictf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = C_TEXT
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: 3-PILLAR STAKEHOLDER STRATEGIC PLAYBOOK
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_canvas(s6)
    add_header(s6, "3-Pillar Stakeholder Strategic Playbook")

    cols = [
        ("HEAD OF MARKETING / CMO", C_CYAN, [
            ("Budget Reallocation (20%)", "Shift ad spend from low-intent cold channels to automated lifecycle retention flows."),
            ("Margin Preservation", "Eliminate blanket promotional discount codes across public marketing channels."),
            ("Tiered Promo Strategy", "Provide exclusive VIP early access to Champions; reserve heavy discounts strictly for At-Risk win-back."),
            ("Target CAC Reduction", "Projected 15-20% CAC efficiency by boosting repeat buyer contribution.")
        ]),
        ("CRM & RETENTION LEAD", C_AMBER, [
            ("Day-14 Trigger Sequence", "Automated email/SMS offering personalized complements based on initial SKU category."),
            ("60-Day Churn Warning", "Trigger high-urgency win-back sequence when customer recency passes 60 days without order."),
            ("Multi-Channel Orchestration", "Deliver high-touch WhatsApp/SMS for At-Risk and curated email digests for Loyalists."),
            ("Segment Re-Scoring", "Recalculate RFM scores weekly to catch segment transitions dynamically.")
        ]),
        ("PRODUCT & GROWTH MANAGER", C_EMERALD, [
            ("Loyalty Gamification", "Implement Bronze, Silver, Gold, Platinum tiers with milestone unlocks on 3rd & 5th orders."),
            ("1-Click Frictionless Reorder", "Add instant repurchase buttons on order history for high-frequency consumable items."),
            ("Tableau Telemetry Hub", "Utilize automated live Tableau ODBC connection to track cohort churn weekly."),
            ("Basket Size Optimization", "Deploy smart checkout cross-sells based on high-affinity product associations.")
        ])
    ]
    col_w = Inches(3.78)
    col_h = Inches(5.6)
    for i, (col_title, col_accent, items) in enumerate(cols):
        cx = Inches(0.8 + i * 3.97)
        ccard = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.4), col_w, col_h)
        set_card_style(ccard, bg_color=C_CARD, border_color=C_BORDER)
        cctf = ccard.text_frame
        cctf.word_wrap = True
        cctf.margin_left = cctf.margin_right = Inches(0.2)
        cctf.margin_top = Inches(0.2)
        cctf.margin_bottom = Inches(0.15)
        
        p = cctf.paragraphs[0]
        p.text = col_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_accent
        p.space_after = Pt(8)
        
        for item_title, item_desc in items:
            ip = cctf.add_paragraph()
            ip.text = f"• {item_title}"
            ip.font.size = Pt(9.5)
            ip.font.bold = True
            ip.font.color.rgb = C_WHITE
            ip.space_before = Pt(6)
            
            idp = cctf.add_paragraph()
            idp.text = f"  {item_desc}"
            idp.font.size = Pt(8.5)
            idp.font.color.rgb = C_MUTED
            idp.space_before = Pt(1)

    # =========================================================================
    # SLIDE 7: TECHNICAL ARCHITECTURE & AUTOMATION WORKFLOW
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_canvas(s7)
    add_header(s7, "Technical Architecture & Automated Data Infrastructure")

    tech_steps = [
        ("1. DATA EXTRACTION & CLEANSING", C_CYAN, [
            "Processed 1.06M raw Excel transactions across 2 sheets.",
            "Filtered invoice cancellations ('C'), negative quantities, and zero prices.",
            "Cleaned 805,549 verified line items with £17.74M revenue."
        ]),
        ("2. SQL & ANALYTICAL MODELING", C_INDIGO, [
            "Engineered SQLite schema (`online_retail_analytics.db`).",
            "Calculated RFM quantiles (`NTILE(5)`) and Cohort Index offsets.",
            "Created indexed views: `v_rfm_summary`, `v_monthly_sales_trend`."
        ]),
        ("3. TABLEAU ODBC AUTOMATION", C_EMERALD, [
            "Auto-configured macOS ODBC DSN (`Portfolio_DB`).",
            "Generated Tableau Data Source (`.tds`) XML for 1-click connection.",
            "Instant launch to Tableau Desktop for visual exploration."
        ]),
        ("4. REPRODUCIBLE ARTIFACTS", C_AMBER, [
            "Production SQL scripts in `/sql/` directory.",
            "Complete Case Study & KPI Scorecard in `README.md`.",
            "High-resolution 300 DPI visualizations & executive PDF report."
        ])
    ]
    tcard_w = Inches(2.78)
    tcard_h = Inches(5.6)
    for i, (st_title, st_col, st_points) in enumerate(tech_steps):
        tx = Inches(0.8 + i * 2.98)
        tcard = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(1.4), tcard_w, tcard_h)
        set_card_style(tcard, bg_color=C_CARD, border_color=C_BORDER)
        tctf = tcard.text_frame
        tctf.word_wrap = True
        tctf.margin_left = tctf.margin_right = Inches(0.18)
        tctf.margin_top = Inches(0.2)
        tctf.margin_bottom = Inches(0.15)
        
        p = tctf.paragraphs[0]
        p.text = st_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = st_col
        p.space_after = Pt(10)
        
        for pt in st_points:
            pp = tctf.add_paragraph()
            pp.text = f"• {pt}"
            pp.font.size = Pt(8.8)
            pp.font.color.rgb = C_TEXT
            pp.space_before = Pt(8)

    pptx_path = os.path.join(PRES_DIR, "Executive_Presentation_Customer_Segmentation_Cohort.pptx")
    prs.save(pptx_path)
    print(f"Professional Slide Deck generated successfully: {pptx_path}")
    return pptx_path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf():
    pdf_path = os.path.join(REPORT_DIR, "Executive_Report_Customer_Segmentation_Cohort.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B')
    )
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=12
    )

    story = []
    story.append(Paragraph("E-Commerce Customer Segmentation & Cohort Analysis", title_style))
    story.append(Paragraph("Executive Briefing & Strategic Retention Playbook | Tackling +25% CAC Surge", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=10))

    story.append(Paragraph("1. Executive Summary & Key Metrics", h2_style))
    story.append(Paragraph(
        "Analysis of 805,549 verified transactions (£17.74M revenue) reveals that 62.4% of revenue is driven by just 28.1% of the customer base (Champions & Loyalists). Meanwhile, the business experiences a steep drop-off at Month 1 (retention drops from 100% to 25.8%).",
        body_style
    ))
    story.append(Spacer(1, 8))

    kpi_data = [
        [Paragraph("<b>Total Revenue</b>", body_style), Paragraph("<b>Analyzed Records</b>", body_style), Paragraph("<b>Unique Customers</b>", body_style), Paragraph("<b>Month-1 Retention</b>", body_style)],
        [Paragraph("<font color='#0284C7' size='12'><b>£17.74M</b></font>", body_style),
         Paragraph("<font color='#0284C7' size='12'><b>805,549</b></font>", body_style),
         Paragraph("<font color='#0284C7' size='12'><b>5,878</b></font>", body_style),
         Paragraph("<font color='#D97706' size='12'><b>25.8%</b></font>", body_style)]
    ]
    t_kpi = Table(kpi_data, colWidths=[130, 130, 130, 130])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. RFM Customer Segmentation Summary", h2_style))
    rfm_table_data = [
        ["Customer Segment", "Count", "% Base", "Total Revenue (£)", "% Revenue", "Avg Recency", "Avg Freq", "Avg Spend"],
        ["Champions", "868", "14.8%", "£7,286,211.20", "41.1%", "12.4 d", "19.8x", "£8,394.25"],
        ["Loyal Customers", "782", "13.3%", "£3,781,402.15", "21.3%", "35.6 d", "7.2x", "£4,835.55"],
        ["At Risk", "945", "16.1%", "£2,684,105.40", "15.1%", "215.8 d", "4.8x", "£2,840.32"],
        ["Potential Loyalists", "741", "12.6%", "£1,452,380.90", "8.2%", "48.2 d", "2.9x", "£1,959.95"],
        ["New Customers", "982", "16.7%", "£1,120,490.15", "6.3%", "24.1 d", "1.4x", "£1,141.03"],
        ["Hibernating / Lost", "1,560", "26.5%", "£1,418,839.38", "8.0%", "442.7 d", "1.3x", "£909.51"]
    ]
    t_rfm = Table(rfm_table_data, colWidths=[95, 45, 45, 95, 55, 60, 55, 70])
    t_rfm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rfm)
    story.append(Spacer(1, 10))

    img_cohort = os.path.join(VIZ_DIR, "01_cohort_retention_heatmap.png")
    if os.path.exists(img_cohort):
        story.append(Paragraph("3. Monthly Cohort Retention Heatmap", h2_style))
        story.append(Image(img_cohort, width=6.8*inch, height=3.2*inch))
        story.append(Spacer(1, 8))

    img_rfm = os.path.join(VIZ_DIR, "02_rfm_revenue_vs_customers.png")
    if os.path.exists(img_rfm):
        story.append(Paragraph("4. Revenue Contribution by Segment", h2_style))
        story.append(Image(img_rfm, width=6.8*inch, height=2.8*inch))
        story.append(Spacer(1, 8))

    story.append(Paragraph("5. Stakeholder Strategic Playbook", h2_style))
    story.append(Paragraph("<b>Head of Marketing & CMO:</b>", body_style))
    story.append(Paragraph("• Shift 20% budget from top-of-funnel mass advertising to automated onboarding and retention.", bullet_style))
    story.append(Paragraph("• Eliminate blanket discounting; restrict discount codes strictly to win-back campaigns for high-spend At Risk accounts.", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>CRM & Retention Lead:</b>", body_style))
    story.append(Paragraph("• Implement a Day-14 post-purchase automated trigger sequence to bridge the Month 1 retention cliff.", bullet_style))
    story.append(Paragraph("• Set up early warning triggers when active customer recency exceeds 60 days without a repurchase.", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Product & Growth Manager:</b>", body_style))
    story.append(Paragraph("• Implement a tiered loyalty gamification system with tangible rewards on 3rd and 5th orders.", bullet_style))
    story.append(Paragraph("• Connect Tableau dashboards via automated TDS / ODBC connection for live weekly cohort tracking.", bullet_style))

    doc.build(story)
    print(f"PDF generated successfully: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_presentation()
    build_pdf()
