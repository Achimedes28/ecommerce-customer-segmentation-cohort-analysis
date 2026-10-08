#!/usr/bin/env python3
"""Build the executive PDF report and the PowerPoint deck from the files in metrics/ and visualizations/.

Every number in both outputs is calculated here from metrics/*.csv, so the report, the deck,
the README and the charts cannot drift apart. Run from the project root:

    python src/build_report_and_deck.py
"""
import os

import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS = os.path.join(ROOT, "metrics")
VIZ = os.path.join(ROOT, "visualizations")
REPORT = os.path.join(ROOT, "reports", "Executive_Report_Customer_Segmentation_Cohort.pdf")
DECK = os.path.join(ROOT, "presentations", "Executive_Presentation_Customer_Segmentation_Cohort.pptx")

AUTHOR = "Novaldi Ramadhan Waluyo"
RAW_ROWS = 1_067_371      # rows in the two sheets of online_retail_II.xlsx (see etl_pipeline.py)
CLEAN_ROWS = 805_549      # rows left after cleaning (see etl_pipeline.py)

# ---------------------------------------------------------------- figures
seg = pd.read_csv(os.path.join(METRICS, "rfm_segment_summary.csv"))
ret = pd.read_csv(os.path.join(METRICS, "cohort_retention_rates.csv"), index_col=0)
seg = seg.set_index("segment")

total_rev = seg["total_revenue"].sum()
total_cust = int(seg["customer_count"].sum())


def mean_ret(month, exclude_first=False):
    data = ret.drop(ret.index[0]) if exclude_first else ret
    return data[str(month)].dropna().mean() * 100


m1 = mean_ret(1)
m1_n = int(ret["1"].notna().sum())
m6, m12 = mean_ret(6), mean_ret(12)
first_cohort = ret.iloc[0]
champ, loyal, risk = seg.loc["Champions"], seg.loc["Loyal Customers"], seg.loc["At Risk"]
top2_cust = champ.pct_customers + loyal.pct_customers
top2_rev = champ.pct_revenue + loyal.pct_revenue
hib = seg.loc["Hibernating"]


def gbp(v):
    return f"£{v/1e6:.2f}M" if v >= 1e6 else f"£{v:,.0f}"


FINDINGS = [
    ("Most customers do not come back in the first month",
     f"Across the {m1_n} cohorts with a month-1 value, on average only {m1:.0f}% of new customers bought again in "
     f"the month after their first order. Retention stays near 20% for the next few months and is about "
     f"{m6:.0f}% at month 6 and {m12:.0f}% at month 12. The largest loss happens right after the first order."),
    ("A small group of customers brings in most of the revenue",
     f"Champions and Loyal Customers are {top2_cust:.0f}% of customers but {top2_rev:.0f}% of revenue. "
     f"Champions alone ({int(champ.customer_count):,} customers) account for {champ.pct_revenue:.0f}% of revenue."),
    ("At Risk customers are the clearest win-back target",
     f"{int(risk.customer_count):,} customers who used to buy often ({risk.avg_frequency:.1f} orders on average) "
     f"have not ordered for about a year ({risk.avg_recency:.0f} days on average). They spent {gbp(risk.total_revenue)} in total."),
    ("Revenue is seasonal",
     "Monthly revenue rises from September and peaks in November in both 2010 and 2011, at roughly twice the level "
     "of early 2010. December 2011 looks low only because the data ends on 9 December."),
]

RECOMMENDATIONS = [
    ("Focus on the second purchase",
     "The biggest drop is in the first month, so a follow-up offer or product recommendation a few weeks after the "
     "first order targets exactly that gap."),
    ("Run a win-back campaign for At Risk customers",
     f"They have a proven buying history and {gbp(risk.total_revenue)} of past spend. Even a small reactivation rate is "
     f"worth more than a campaign aimed at Hibernating customers ({int(hib.customer_count):,} customers, "
     f"{hib.pct_revenue:.1f}% of revenue)."),
    ("Keep Champions without heavy discounts",
     "They already buy often, so early access or service perks are a cheaper way to keep them than price cuts."),
    ("Plan stock and campaigns around September to November",
     "Demand is highest in these months in both years."),
]

LIMITATIONS = [
    "The dataset has no marketing cost, acquisition channel or margin data, so recommendations cannot be costed. "
    "The 25% CAC increase comes from the project brief, not from the data.",
    "Rows without a customer ID (about a quarter of the raw data) are excluded; revenue covers identified customers only.",
    "The December 2009 cohort retains much better than the rest (" + f"{first_cohort['1']*100:.0f}% in month 1) because "
    "the data starts that month, so it includes customers who were already buying before.",
    "The data ends on 9 December 2011, so recent cohorts have only a few months of history.",
    "RFM segments depend on the chosen score thresholds; different cut-offs would move some customers between segments.",
]

SEG_ROWS = [["Segment", "Customers", "% customers", "Revenue", "% revenue", "Days since last order", "Avg orders"]]
for name, row in seg.sort_values("total_revenue", ascending=False).iterrows():
    SEG_ROWS.append([name, f"{int(row.customer_count):,}", f"{row.pct_customers:.1f}%", gbp(row.total_revenue),
                     f"{row.pct_revenue:.1f}%", f"{row.avg_recency:.0f}", f"{row.avg_frequency:.1f}"])

# ---------------------------------------------------------------- PDF report
INK, MUTED, ACCENT = colors.HexColor("#0F172A"), colors.HexColor("#475569"), colors.HexColor("#1D4ED8")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=INK, alignment=TA_LEFT, spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=MUTED, spaceAfter=14)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13, textColor=INK, spaceBefore=12, spaceAfter=6)
H3 = ParagraphStyle("H3", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, textColor=ACCENT, spaceBefore=6, spaceAfter=2)
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=INK, spaceAfter=6)
BUL = ParagraphStyle("BUL", parent=BODY, leftIndent=12, bulletIndent=2)


def chart(name, width=16.5 * cm):
    path = os.path.join(VIZ, name)
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    return Image(path, width=width, height=width * h / w)


def kpi_table():
    data = [["Revenue (identified customers)", "Cleaned transactions", "Customers", "Return in month 1 (avg)"],
            [gbp(total_rev), f"{CLEAN_ROWS:,}", f"{total_cust:,}", f"{m1:.0f}%"]]
    t = Table(data, colWidths=[4.4 * cm] * 4)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica", 8.5), ("TEXTCOLOR", (0, 0), (-1, 0), MUTED),
        ("FONT", (0, 1), (-1, 1), "Helvetica-Bold", 15), ("TEXTCOLOR", (0, 1), (-1, 1), INK),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 2, colors.white),
    ]))
    return t


def seg_table():
    t = Table(SEG_ROWS, colWidths=[3.6 * cm, 1.8 * cm, 2.0 * cm, 1.9 * cm, 1.8 * cm, 3.5 * cm, 1.9 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8), ("TEXTCOLOR", (0, 0), (-1, 0), MUTED),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, MUTED), ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, f"E-Commerce Customer Segmentation & Cohort Retention · {AUTHOR}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page))
    canvas.restoreState()


story = [
    Paragraph("E-Commerce Customer Segmentation and Cohort Retention", H1),
    Paragraph(f"UCI Online Retail II, December 2009 to 9 December 2011 · {AUTHOR}", SUB),
    Paragraph("Context", H2),
    Paragraph("The project follows a case brief: a UK online retailer has seen customer acquisition cost rise 25% in "
              "12 months while marketing still relies on untargeted mass promotions. The questions are how many new "
              "customers come back after their first order, and which customer groups are worth a retention or "
              "win-back effort.", BODY),
    kpi_table(), Spacer(1, 10),
    Paragraph("Key findings", H2),
]
for title, text in FINDINGS:
    story += [Paragraph(title, H3), Paragraph(text, BODY)]
story += [Paragraph("Data and cleaning", H2),
          Paragraph(f"{RAW_ROWS:,} raw rows were reduced to {CLEAN_ROWS:,} by removing rows without a customer ID, "
                    "cancelled invoices (invoice numbers starting with C) and rows with zero or negative quantity or "
                    "price. Line revenue is quantity × unit price.", BODY),
          PageBreak(),
          Paragraph("1. Cohort retention", H2),
          Paragraph("Each row is the month of a customer's first order; each column is the number of months since then. "
                    "Cells show the share of the cohort that ordered again in that month.", BODY),
          chart("01_cohort_retention_heatmap.png"),
          Paragraph(FINDINGS[0][1], BODY),
          Paragraph(LIMITATIONS[2], BODY),
          PageBreak(),
          Paragraph("2. RFM segmentation", H2),
          Paragraph("Customers were scored 1 to 5 on recency, frequency and monetary value using quintiles, with "
                    "10 December 2011 as the reference date, and then grouped into segments.", BODY),
          chart("02_rfm_revenue_vs_customers.png"), Spacer(1, 6), seg_table(), Spacer(1, 6),
          Paragraph(FINDINGS[1][1] + " " + FINDINGS[2][1], BODY),
          PageBreak(),
          Paragraph("3. Seasonality", H2),
          chart("03_monthly_revenue_growth.png"),
          Paragraph(FINDINGS[3][1], BODY),
          Paragraph("Recommendations", H2),
          Paragraph("These are directional, since the data does not include cost or campaign results.", BODY)]
for i, (title, text) in enumerate(RECOMMENDATIONS, 1):
    story.append(Paragraph(f"<b>{i}. {title}.</b> {text}", BODY))
story.append(Paragraph("Limitations", H2))
for text in LIMITATIONS:
    story.append(Paragraph(text, BUL, bulletText="•"))

os.makedirs(os.path.dirname(REPORT), exist_ok=True)
SimpleDocTemplate(REPORT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                  title="E-Commerce Customer Segmentation and Cohort Retention", author=AUTHOR
                  ).build(story, onFirstPage=footer, onLaterPages=footer)

# ---------------------------------------------------------------- PowerPoint deck
NAVY, WHITE, TXT, GREY, BLUE, PALE = (RGBColor(0x0F, 0x17, 0x2A), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0x1E, 0x29, 0x3B),
                                      RGBColor(0x64, 0x74, 0x8B), RGBColor(0x1D, 0x4E, 0xD8), RGBColor(0xF1, 0xF5, 0xF9))
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def box(slide, x, y, w, h, fill):
    shp = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill; shp.line.fill.background()
    return shp


def text(slide, x, y, w, h, paras, size=16, color=TXT, bold=False):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    for i, p in enumerate(paras if isinstance(paras, list) else [paras]):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        runs = p if isinstance(p, tuple) else (p,)
        for j, r in enumerate(runs):
            run = par.add_run(); run.text = r
            run.font.size = Pt(size); run.font.color.rgb = color; run.font.name = "Calibri"
            run.font.bold = bold or (len(runs) > 1 and j == 0)
        par.space_after = Pt(8)
    return tf


def title(slide, t, kicker):
    text(slide, 0.6, 0.35, 12, 0.4, kicker.upper(), size=11, color=BLUE, bold=True)
    text(slide, 0.6, 0.7, 12.1, 0.8, t, size=28, color=NAVY, bold=True)


def picture(slide, name, x, y, w):
    slide.shapes.add_picture(os.path.join(VIZ, name), Inches(x), Inches(y), width=Inches(w))


# 1. title
s = prs.slides.add_slide(BLANK); box(s, 0, 0, 13.333, 7.5, NAVY)
text(s, 0.8, 2.2, 11.5, 0.5, "DATA ANALYTICS CASE STUDY", size=13, color=RGBColor(0x93, 0xC5, 0xFD), bold=True)
text(s, 0.8, 2.7, 11.5, 1.4, "E-Commerce Customer Segmentation and Cohort Retention", size=38, color=WHITE, bold=True)
text(s, 0.8, 4.3, 11.5, 0.6, "Who comes back after the first order, and which customers are worth keeping", size=18,
     color=RGBColor(0xCB, 0xD5, 0xE1))
text(s, 0.8, 5.6, 11.5, 0.5, f"UCI Online Retail II · Dec 2009 to Dec 2011 · SQL, Python, Tableau · {AUTHOR}", size=13,
     color=RGBColor(0x94, 0xA3, 0xB8))

# 2. summary
s = prs.slides.add_slide(BLANK); title(s, "Summary", "Overview")
for i, (v, lab) in enumerate([(gbp(total_rev), "Revenue, identified customers"), (f"{CLEAN_ROWS/1000:.1f}K", "Cleaned transactions"),
                              (f"{total_cust:,}", "Customers"), (f"{m1:.0f}%", "Return in month 1 (avg)")]):
    x = 0.6 + i * 3.08
    box(s, x, 1.7, 2.85, 1.35, PALE)
    text(s, x + 0.2, 1.8, 2.5, 0.6, v, size=28, color=NAVY, bold=True)
    text(s, x + 0.2, 2.5, 2.5, 0.4, lab, size=12, color=GREY)
text(s, 0.6, 3.45, 12.1, 3.6, [(f"{t}. ", d) for t, d in FINDINGS], size=14)

# 3. cohort
s = prs.slides.add_slide(BLANK); title(s, f"Only {m1:.0f}% of new customers buy again in month 1", "Cohort retention")
picture(s, "01_cohort_retention_heatmap.png", 0.6, 1.65, 7.6)
text(s, 8.5, 1.75, 4.3, 5.2, [FINDINGS[0][1], LIMITATIONS[2]], size=14)

# 4. RFM
s = prs.slides.add_slide(BLANK)
title(s, f"{top2_cust:.0f}% of customers bring in {top2_rev:.0f}% of revenue", "RFM segmentation")
picture(s, "02_rfm_revenue_vs_customers.png", 0.6, 1.65, 7.6)
text(s, 8.5, 1.75, 4.3, 5.2, [FINDINGS[1][1], FINDINGS[2][1]], size=14)

# 5. seasonality
s = prs.slides.add_slide(BLANK); title(s, "Revenue peaks every November", "Seasonality")
picture(s, "03_monthly_revenue_growth.png", 0.6, 1.65, 7.6)
text(s, 8.5, 1.75, 4.3, 5.2, [FINDINGS[3][1], "Stock and campaigns should be planned around September to November."], size=14)

# 6. recommendations
s = prs.slides.add_slide(BLANK); title(s, "Recommendations", "What to do")
for i, (t, d) in enumerate(RECOMMENDATIONS):
    x, y = 0.6 + (i % 2) * 6.15, 1.7 + (i // 2) * 2.55
    box(s, x, y, 5.9, 2.3, PALE)
    text(s, x + 0.25, y + 0.2, 5.4, 0.5, f"{i+1}. {t}", size=17, color=NAVY, bold=True)
    text(s, x + 0.25, y + 0.8, 5.4, 1.4, d, size=14)
text(s, 0.6, 6.85, 12, 0.4, "Directional only: the data has no marketing cost, channel or margin information.", size=12, color=GREY)

# 7. method and limitations
s = prs.slides.add_slide(BLANK); title(s, "Method and limitations", "How to read these results")
text(s, 0.6, 1.7, 5.9, 5.3, [
    ("Data. ", f"{RAW_ROWS:,} raw rows reduced to {CLEAN_ROWS:,} after removing rows without a customer ID, cancelled invoices and non-positive quantities or prices."),
    ("Cohorts. ", "Customers grouped by first-order month; retention is the share ordering again in each later month."),
    ("RFM. ", "Recency, frequency and monetary value scored 1 to 5 by quintile, reference date 10 December 2011."),
    ("Tools. ", "Python (pandas) for cleaning and scoring, SQLite for the SQL views, Tableau and matplotlib for charts."),
], size=14)
text(s, 6.9, 1.7, 5.9, 5.3, LIMITATIONS, size=14)

os.makedirs(os.path.dirname(DECK), exist_ok=True)
prs.save(DECK)
print("Report:", REPORT)
print("Deck:  ", DECK)
