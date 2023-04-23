import pandas as pd
import json
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Image

from format_data import import_data, takes_data, plot_series

file_list = ['takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010', 'takes202104', 'takes202110', 'takes202204', 'takes202210']
manad_lista = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
num_obs = len(file_list)
artal = file_list[num_obs-1][5:9]
artal_int = int(artal)
manad = int(file_list[num_obs-1][9:11])

if manad == 4:
    period_text = f"vinterhalvåret {str(artal_int-1)}/{artal[2:]}"
else:
    period_text = f"sommarhalvåret {artal}"

df = import_data(file_list)
df_counts = takes_data(df)
print(df_counts)
df_counts_trans = df_counts.transpose()



df_halfyear = df
for i in range(1,num_obs):
    halfyear_col_name = file_list[i]+'halfyear'
    df_halfyear[halfyear_col_name] = df_halfyear[file_list[i]]-df_halfyear[file_list[i-1]]


top10_takes_last_six_months = df[halfyear_col_name].nlargest(10).astype(int)
top10_takes_total = df[file_list[num_obs-1]].nlargest(10).astype(int)

#print(top10_takes_last_six_months)

# Create a PDF document with A4 size
doc = SimpleDocTemplate("turfrapport.pdf", pagesize=A4)

# Set up styles
styles = getSampleStyleSheet()
style_title = styles['Title']
#style_bold = styles['Bold']
style_normal = styles['Normal']
style_small_title = styles['Heading2']


# Create content for the report
heading = Paragraph(f"Turfrapport {manad_lista[manad-1]} {artal}", style_title)
zone_list = top10_takes_last_six_months.index.values
#print(zone_list)

#zone_list = list()
#if len(df[df['takes202210halfyear']==top10_takes_last_six_months[0]].index) > 0:
#    zone_name = df[df['takes202210halfyear']==top10_takes_last_six_months[0]].index[0]
#else:
#    zone_name = ""
total_t0 = df_counts_trans['Totalt'][num_obs-1]
total_t1 = df_counts_trans['Totalt'][num_obs-2]
total_t2 = df_counts_trans['Totalt'][num_obs-3]
total_t3 = df_counts_trans['Totalt'][num_obs-4]
nya_unika_t0 = total_t0 - total_t1
nya_unika_t1 = total_t1 - total_t2
nya_unika_t2 = total_t2 - total_t3

introtext = f"De senaste 6 månadernas turfande var {top10_takes_last_six_months.index.values[0]} den vanligaste zonen med {top10_takes_last_six_months[0]} besök. "
if(top10_takes_last_six_months.index.values[0] == top10_takes_total.index.values[0]):
    introtext = introtext + f" Även den totalt vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
else:
    introtext = introtext + f" Den totalt sett vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
introtext = introtext + f" Totalt togs {nya_unika_t0} nya unika zoner under {period_text}, jämfört med {nya_unika_t1} under halvåret innan."
intro_paragraph = Paragraph(introtext, style_normal)

wardedfarger_heading = Paragraph("Wardedfärger", style_small_title)

wardedtext = "I detta avsnitt kommer information om hur många zoner som har respektive wardedfärg. "
wardedtext = wardedtext + "Förutom de vanliga färgerna grön, gul, röd och lila, så har de lila zonerna delats upp i 51-100, 101-250, 251-500, 501-1000 och 1001+. "
wardedtext = wardedtext + ""
warded_paragraph = Paragraph(wardedtext, style_normal)

table_data = [list(df_counts.columns)] + [list(row) for row in df_counts.values]
table = Table(table_data)
# Add style to the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
    ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, -1), (-1, -1), 14),
    ('TOPPADDING', (0, -1), (-1, -1), 12),
])

# Apply style to the table
table.setStyle(style)

print(table)

plot_series(df_counts_trans['1'],df_counts_trans['2 - 10'],df_counts_trans['11 - 20'], filename = '1till20.png')
diagram_1till20 = Image("1till20.png", width = 10*cm, height = 7 * cm)

# Build the report content
flowables = [heading, intro_paragraph, wardedfarger_heading, warded_paragraph, table, diagram_1till20]

# Set up the document and write the content
doc.build(flowables)


#plt2 = plot_series(df_counts_trans['501 - 1000'],df_counts_trans['1001+'])

#plt1.show()
#plt2.show()
