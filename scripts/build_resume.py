from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS = [OUTPUT_DIR / "Regina_Jin_Resume.pdf", ROOT / "cv.pdf"]

PAGE_WIDTH, PAGE_HEIGHT = A4
NAVY = colors.HexColor("#153746")
TEAL = colors.HexColor("#008E83")
TEXT = colors.HexColor("#213640")
MUTED = colors.HexColor("#627580")
LIGHT = colors.HexColor("#D8E5E8")

styles = getSampleStyleSheet()
name_style = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=23,
    leading=25,
    alignment=TA_CENTER,
    textColor=NAVY,
    spaceAfter=4,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.2,
    leading=10.2,
    alignment=TA_CENTER,
    textColor=MUTED,
    spaceAfter=1,
)
summary_style = ParagraphStyle(
    "Summary",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.45,
    leading=11.2,
    alignment=TA_LEFT,
    textColor=TEXT,
    spaceAfter=3,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=12,
    textColor=NAVY,
    tracking=0.8,
    spaceBefore=5,
    spaceAfter=1,
)
entry_title_style = ParagraphStyle(
    "EntryTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.9,
    leading=10.4,
    textColor=NAVY,
)
entry_meta_style = ParagraphStyle(
    "EntryMeta",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=7.9,
    leading=9.5,
    textColor=MUTED,
)
right_title_style = ParagraphStyle(
    "RightTitle",
    parent=entry_title_style,
    alignment=TA_RIGHT,
)
right_meta_style = ParagraphStyle(
    "RightMeta",
    parent=entry_meta_style,
    alignment=TA_RIGHT,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.15,
    leading=10.5,
    leftIndent=9,
    firstLineIndent=-6,
    textColor=TEXT,
    spaceBefore=1.2,
    spaceAfter=0.7,
)
compact_style = ParagraphStyle(
    "Compact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.1,
    leading=10.4,
    textColor=TEXT,
    spaceAfter=1.5,
)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def section(title: str):
    return [
        Paragraph(title.upper(), section_style),
        HRFlowable(width="100%", thickness=0.7, color=TEAL, spaceBefore=0, spaceAfter=3),
    ]


def entry(company, location, role, dates, bullets, link=None):
    company_markup = esc(company)
    if link:
        company_markup = f'<link href="{link}" color="#153746">{company_markup}</link>'
    header = Table(
        [
            [Paragraph(company_markup, entry_title_style), Paragraph(esc(location), right_title_style)],
            [Paragraph(esc(role), entry_meta_style), Paragraph(esc(dates), right_meta_style)],
        ],
        colWidths=[118 * mm, 54 * mm],
        hAlign="LEFT",
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    blocks = [header]
    blocks.extend(Paragraph(f"• {bullet}", bullet_style) for bullet in bullets)
    blocks.append(Spacer(1, 2.4))
    return KeepTogether(blocks)


def education_entry(school, location, degree, dates):
    table = Table(
        [
            [Paragraph(esc(school), entry_title_style), Paragraph(esc(location), right_title_style)],
            [Paragraph(esc(degree), entry_meta_style), Paragraph(esc(dates), right_meta_style)],
        ],
        colWidths=[118 * mm, 54 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return [table, Spacer(1, 2.2)]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 12.5 * mm, PAGE_WIDTH - 20 * mm, 12.5 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 8.5 * mm, "Regina Jin | Product, AI, Spatial Data, and Growth")
    page = f"{doc.page} / 2"
    canvas.drawRightString(PAGE_WIDTH - 20 * mm, 8.5 * mm, page)
    canvas.restoreState()


def build(path: Path):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=14 * mm,
        bottomMargin=17 * mm,
        title="Resume of Regina Jin",
        author="Regina Jin",
        subject="Product, AI, spatial data, business development, and startup experience",
    )

    story = [
        Paragraph("Regina Jin", name_style),
        Paragraph(
            '858-261-8053 &nbsp;&nbsp;|&nbsp;&nbsp; '
            '<link href="mailto:Reginaji@usc.edu" color="#008E83">Reginaji@usc.edu</link> &nbsp;&nbsp;|&nbsp;&nbsp; '
            '<link href="https://reginajin168.github.io" color="#008E83">reginajin168.github.io</link>',
            contact_style,
        ),
        Paragraph(
            '<link href="https://www.linkedin.com/in/regina-jin188" color="#008E83">linkedin.com/in/regina-jin188</link>',
            contact_style,
        ),
        Spacer(1, 4),
    ]

    story.extend(section("Profile"))
    story.append(
        Paragraph(
            "Product builder and spatial data scientist with experience across AI products, cross-border business development, and technical delivery. Co-founder of William AI, combining hands-on software development with user discovery, community building, and product-led growth.",
            summary_style,
        )
    )

    story.extend(section("Education"))
    story.extend(
        education_entry(
            "University of Southern California (USC)",
            "Los Angeles, USA",
            "M.S. in Spatial Data Science",
            "Jan 2026 - Present",
        )
    )
    story.extend(
        education_entry(
            "Hangzhou Normal University",
            "Hangzhou, China",
            "B.S. in Geographic Information Science",
            "Sep 2021 - Jun 2025",
        )
    )

    story.extend(section("Professional Experience"))
    story.append(
        entry(
            "UniUni",
            "Remote",
            "Specialist of Region Expansion & CDC (Intern)",
            "Jul 2026 - Present",
            [
                "Built a cross-border prospecting pipeline by screening approximately <b>5,000 logistics companies</b> across North America and Europe and identifying decision-makers in operations, supply chain, and partnerships.",
                "Executed approximately <b>3,500 targeted outreach attempts</b>; converted all 3 responses into discovery meetings, achieving a <b>100% response-to-meeting conversion rate</b>.",
                "Qualified partnership interest and documented account intelligence to support regional expansion and last-mile logistics business development.",
            ],
        )
    )
    story.append(
        entry(
            "William AI",
            "Los Angeles / Remote",
            "Co-founder & Product Lead",
            "May 2026 - Present",
            [
                "Co-founded an AI-powered emotional wellness product that combines guided AI support with community-based engagement.",
                "Led the product from concept through <b>Alpha testing</b>; owned requirements, software development, user feedback loops, community operations, and the post-launch growth roadmap.",
                "Built a pre-launch community and acquired <b>2,000+ waitlist signups</b> ahead of public release.",
            ],
            link="https://www.iamwilliam.xyz",
        )
    )
    story.append(
        entry(
            "University of Southern California - Spatial Sciences Institute",
            "Los Angeles, USA",
            "Graduate Research Assistant",
            "Mar 2026 - Present",
            [
                "Develop interactive GIS web applications using React and Mapbox/ArcGIS APIs to visualize complex spatial datasets for urban research.",
                "Architect spatial data pipelines and optimize PostGIS/PostgreSQL databases for large-scale geographic features.",
            ],
        )
    )
    story.append(
        entry(
            "Huaxin Consulting Co., Ltd.",
            "Hangzhou, China",
            "Product Manager / Project Manager",
            "Jun 2025 - Dec 2025",
            [
                "Led the end-to-end lifecycle of 3 digital products, achieving <b>100% on-time delivery</b> and <b>90% client satisfaction</b>.",
                "Seconded to China Telecom AI Co. for the Xirang MaaS platform; resolved <b>12+ critical</b> compatibility and permission issues and accelerated module integration by 3 days.",
                "Delivered English technical pitches to international stakeholders and secured <b>2 cooperation agreements</b>.",
            ],
        )
    )

    story.append(PageBreak())
    story.extend(section("Earlier Experience"))
    story.append(
        entry(
            "Huaxin Consulting Co., Ltd.",
            "Hangzhou, China",
            "Data Engineering & AI Product Intern",
            "Dec 2024 - May 2025",
            [
                "Designed tokenization and cleaning logic for a Government GenAI model across <b>2,000,000+ records</b>, improving Precision and Recall by 12%.",
                "Developed a distributed Java crawler for 31 bidding platforms and Python validation scripts with <b>&lt;1% amount error</b> and 90% clause coverage.",
            ],
        )
    )
    story.append(
        entry(
            "Ouhai Surveying and Mapping Institute",
            "Wenzhou, China",
            "Spatial Data Analyst Intern",
            "Jun 2024 - Sep 2024",
            [
                "Processed <b>100GB+</b> of multi-source satellite remote sensing data using Python and produced 20+ visualization dashboards.",
                "Built ArcGIS-based spatial models that increased land-area calculation efficiency by <b>30%</b> for government planning decisions.",
            ],
        )
    )

    story.extend(section("Selected Projects"))
    story.append(
        entry(
            'Telecom "Xirang" MaaS Platform',
            "AI Infrastructure",
            "Technical Project Manager",
            "Aug 2025 - Nov 2025",
            [
                "Co-led adaptation between the MaaS layer and AI infrastructure; managed development sprints across 8 workstreams and delivered key modules 3 days ahead of schedule."
            ],
        )
    )
    story.append(
        entry(
            "Marine Eco-Remote Sensing Big Data System",
            "National Grand Prize",
            "Core Member / Product Manager / Data Analyst",
            "Jun 2024 - Jan 2025",
            [
                "Improved LSTM forecasting accuracy by <b>10%</b>, processed 100GB+ of spatial data, and coordinated cross-functional product delivery.",
                "Won <b>1st Place</b> in the 19th Challenge Cup Special Competition among 7,000+ national teams.",
            ],
        )
    )
    story.append(
        entry(
            "Intelligent UAV Collaborative Management System",
            "National Third Prize",
            "Team Leader / Product Manager",
            "Jul 2023 - Jun 2024",
            [
                "Led market research, system architecture, and the product roadmap for multi-UAV coordination; ranked in the top 3% of 8,801 national teams."
            ],
        )
    )

    story.extend(section("Research & Publications"))
    story.append(
        Paragraph(
            '<b>Co-author:</b> "Assessment of Satellite Products in Estimating Tropical Cyclone Remote Precipitation over the Yangtze River Delta Region," <i>Atmosphere</i>, 2024 (SCI, IF: 2.9).',
            compact_style,
        )
    )
    story.append(
        Paragraph(
            '<b>Co-author:</b> "Multi-source Remote Sensing Monitoring Methods for Water Quality in Wetland Lake Chains...", <i>Journal of Hangzhou Normal University</i>, 2024.',
            compact_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Software copyrights:</b> Lead author of 3 registered remote-sensing software systems covering algae bloom inversion, water color index extraction, and aerosol optical depth inversion.",
            compact_style,
        )
    )

    story.extend(section("Skills"))
    skills = [
        ("Product & Growth", "Product strategy, requirement engineering, user discovery, Alpha testing, community operations, product-led growth"),
        ("Business Development", "Market research, account intelligence, decision-maker mapping, targeted outreach, lead qualification"),
        ("Data & AI", "Python, SQL, LSTM, predictive modeling, data cleaning, GenAI product development"),
        ("Geospatial", "ArcGIS Pro, ENVI, remote sensing, digital twin, spatial analysis"),
        ("Languages", "Native Mandarin; English - TOEFL 102, GRE 326"),
    ]
    for label, value in skills:
        story.append(Paragraph(f"<b>{label}:</b> {value}", compact_style))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    for output in OUTPUTS:
        build(output)
        print(output)
