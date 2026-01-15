from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def generate_sustainability_report(analytics_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12
    )
    
    title = Paragraph("Sustainability Report", title_style)
    story.append(title)
    
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
    story.append(date_text)
    story.append(Spacer(1, 0.3*inch))
    
    summary_heading = Paragraph("Executive Summary", heading_style)
    story.append(summary_heading)
    
    key_metrics = analytics_data['key_metrics']
    summary_data = [
        ['Metric', 'Value'],
        ['Total Materials Analyzed', str(key_metrics['total_materials'])],
        ['CO₂ Reduction', f"{key_metrics['co2_saved_percent']}%"],
        ['Cost Savings', f"₹{key_metrics['cost_saved']:.2f}"],
        ['Eco-Friendly Materials', f"{key_metrics['eco_friendly_percent']}%"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    co2_heading = Paragraph("CO₂ Reduction Analysis", heading_style)
    story.append(co2_heading)
    
    co2_data = analytics_data['co2_reduction']
    co2_text = Paragraph(
        f"By choosing eco-friendly materials, an average CO₂ reduction of <b>{co2_data['reduction_percent']}%</b> "
        f"can be achieved. This translates to <b>{co2_data['total_saved']} kg</b> of CO₂ saved per packaging unit.",
        styles['Normal']
    )
    story.append(co2_text)
    story.append(Spacer(1, 0.2*inch))
    
    cost_heading = Paragraph("Cost Savings Analysis", heading_style)
    story.append(cost_heading)
    
    cost_data = analytics_data['cost_savings']
    cost_text = Paragraph(
        f"Budget-conscious material selection can save approximately <b>₹{cost_data['total_saved']:.2f}</b> "
        f"per unit, representing a <b>{cost_data['savings_percent']}%</b> cost reduction.",
        styles['Normal']
    )
    story.append(cost_text)
    story.append(Spacer(1, 0.3*inch))
    
    rec_heading = Paragraph("Recommendations", heading_style)
    story.append(rec_heading)
    
    recommendations = [
        "Prioritize recyclable and biodegradable materials for environmental sustainability",
        "Consider durability scores for products requiring long-distance shipping",
        "Balance cost and environmental impact based on product requirements",
        "Regularly review material options as new sustainable alternatives become available"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        rec_para = Paragraph(f"{i}. {rec}", styles['Normal'])
        story.append(rec_para)
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
