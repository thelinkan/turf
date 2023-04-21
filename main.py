import pandas as pd
import json
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate

from format_data import import_data, takes_data, plot_series

file_list = ['takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010']#, 'takes202104', 'takes202110', 'takes202204', 'takes202210']
manad_lista = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
num_obs = len(file_list)
artal = file_list[num_obs-1][5:9]
manad = int(file_list[num_obs-1][9:11])


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
introtext = f"De senaste 6 månadernas turfande var {top10_takes_last_six_months.index.values[0]} den vanligaste zonen med {top10_takes_last_six_months[0]} besök. "
if(top10_takes_last_six_months.index.values[0] == top10_takes_total.index.values[0]):
    introtext = introtext + f" Även den totalt vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
else:
    introtext = introtext + f" Den totalt sett vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
    
intro_paragraph = Paragraph(introtext, style_normal)
# Build the report content
flowables = [heading, intro_paragraph]

# Set up the document and write the content
doc.build(flowables)


#plt1 = plot_series(df_counts_trans['1'],df_counts_trans['2 - 10'])
#plt2 = plot_series(df_counts_trans['501 - 1000'],df_counts_trans['1001+'])

#plt1.show()
#plt2.show()
