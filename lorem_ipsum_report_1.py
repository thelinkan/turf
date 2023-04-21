# Import the required libraries
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import matplotlib.pyplot as plt
import pandas as pd
from loremipsum import get_paragraphs

# Create a Pandas DataFrame for the sales data
data = {'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Sales': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210],
        'Revenue': [20000, 22000, 24000, 26000, 28000, 30000, 32000, 34000, 36000, 38000, 40000, 42000]}
df = pd.DataFrame(data)

# Define the page size
PAGE_WIDTH, PAGE_HEIGHT = letter

# Create a new SimpleDocTemplate object
doc = SimpleDocTemplate("turf_report.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

# Define the styles for the report
styles = getSampleStyleSheet()
style_title = styles['Title']
style_text = styles['Normal']

# Generate some Lorem ipsum text
lorem_text = get_paragraphs(1)[0]

# Create the list of flowables to add to the document
flowables = []

# Add the title to the document
title = Paragraph("Sales Report", style_title)
flowables.append(title)
flowables.append(Spacer(1, 0.5 * inch))

# Add the text to the document
text = Paragraph(lorem_text, style_text)
flowables.append(text)
flowables.append(Spacer(1, 0.5 * inch))

# Create the first diagram and add it to the document
plt.figure(figsize=(6, 4))
plt.plot(df['Month'], df['Sales'])
plt.title('Monthly Sales', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Sales', fontsize=12)
plt.tight_layout()
plt.savefig('sales_diagram_1.png', dpi=300)
plt.close()

sales_diagram_1 = Image('sales_diagram_1.png', width=5 * inch, height=3 * inch)
flowables.append(sales_diagram_1)
flowables.append(Spacer(1, 0.5 * inch))

# Add more text to the document
text = Paragraph(get_paragraphs(1)[0], style_text)
flowables.append(text)
flowables.append(Spacer(1, 0.5 * inch))

# Create the second diagram and add it to the document
plt.figure(figsize=(6, 4))
plt.plot(df['Month'], df['Revenue'])
plt.title('Monthly Revenue', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue', fontsize=12)
plt.tight_layout()
plt.savefig('sales_diagram_2.png', dpi=300)
plt.close()

sales_diagram_2 = Image('sales_diagram_2.png', width=5 * inch, height=3 * inch)
flowables.append(sales_diagram_2)

# Build the document and save the PDF file
doc.build(flowables)
