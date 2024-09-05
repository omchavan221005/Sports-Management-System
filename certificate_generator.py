import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfgen import canvas

def generate_certificate(winner_details):
    # Define the filename and path
    dir_path = r'c:\Users\KRRISH\OneDrive\Desktop\PYTHON TUTORIAL'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)  # Create the directory if it does not exist
    
    # Check if 'certificate_details' key exists
    certificate_details = winner_details.get('certificate_details', {})
    team_name = certificate_details.get('team_name', 'Unknown_Team')
    event = certificate_details.get('event', 'Unknown_Event')

    file_name = os.path.join(dir_path, f"{team_name}_Certificate.pdf")
    
    # Create the PDF document
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []

    # Define styles
    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        fontSize=24,
        alignment=1
    )
    content_style = ParagraphStyle(
        'Content',
        parent=getSampleStyleSheet()['BodyText'],
        fontSize=14,
        alignment=1
    )
    date_style = ParagraphStyle(
        'Date',
        parent=getSampleStyleSheet()['BodyText'],
        fontSize=12,
        alignment=1
    )

    # Create the PDF with canvas to draw the border
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(0.5 * inch, 0.5 * inch, width - inch, height - inch, stroke=1, fill=0)
    c.save()

    # Add certificate content
    elements.append(Spacer(1, 1.5 * inch))
    elements.append(Paragraph("Certificate of Achievement", title_style))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(
        f"This is to certify that <b>{team_name}</b> has won the <b>{event}</b>.",
        content_style
    ))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Date: 2024", date_style))
    
    # Build the PDF
    doc.build(elements)
    
    return file_name
