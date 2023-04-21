from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate

# Create a PDF document with A4 size
doc = SimpleDocTemplate("example.pdf", pagesize=A4)

# Set up styles
styles = getSampleStyleSheet()
style_title = styles['Title']
#style_bold = styles['Bold']
style_normal = styles['Normal']
style_small_title = styles['Heading2']

# Create content for the report
heading = Paragraph("My Report", style_title)

bold_text = "This is a bold text. This is a bold text. This is a bold text. This is a bold text."
bold_paragraph = Paragraph(bold_text, style_normal)

normal_text = "This is a non-bold text. This is a non-bold text. This is a non-bold text. This is a non-bold text."
normal_paragraph = Paragraph(normal_text, style_normal)

small_heading = Paragraph("Section 1", style_small_title)

normal_text2 = "This is another non-bold text. This is another non-bold text. This is another non-bold text. This is another non-bold text."
normal_paragraph2 = Paragraph(normal_text2, style_normal)

# Build the report content
flowables = [heading,
             bold_paragraph,
             normal_paragraph,
             small_heading,
             normal_paragraph2]

# Set up the document and write the content
doc.build(flowables)
