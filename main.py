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

from format_data import takes_data, plot_series, plot_stacked_series, plot_stacked_area
from console_output import print_df
from report_text import create_introtext, create_wardedtext, create_halfyeartext, create_newtext, create_totaltext, create_interactiontext
from report_text import create_regionaltext
from report_text import periodtext, periodtext_kort, prev_period
from turf_data import TurfData
from styles import style, style_top10, styles, style_normal,style_small_title,style_title

turfname='TheLinkan'

file_list = ['takes201610', 'takes201704','takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010', 'takes202104', 'takes202110', 'takes202204', 'takes202210', 'takes202304', 'takes202310', 'takes202404', 'takes202410']
manad_lista = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
num_obs: int = len(file_list)
artal = file_list[num_obs-1][5:9]
artal_int = int(artal)
manad = int(file_list[num_obs-1][9:11])

turfdata = TurfData(turfname, artal_int, manad)
print(turfdata.turfname)

# Importera data 
turfdata.import_main_dfs(file_list)

pd.options.display.float_format = '{:,.0f}'.format

print_df(turfdata.df_takes,"Main df")

turfdata.set_df_count_takes()
print_df(turfdata.df_count_takes,"df_counts")

print_df(turfdata.df_count_takes_trans,"df_counts_trans - class")

turfdata.df_takes.to_excel("c:/temp/df.xlsx")

print_df(turfdata.df_takes_halfyear,"df_halfyear - class")

# Länder och regioner
turfdata.create_df_countries_regions(file_list)

print_df(turfdata.df_countries_off,"df_countries_off")
print_df(turfdata.df_sverige_areas,"df_sverige_areas")
turfdata.df_sverige_areas.to_excel("c:/temp/df_sverige_areas.xlsx")

print(f"100% - {turfdata.num_sv_areas_100}")
print(f"80% - 100% - {turfdata.num_sv_areas_80_100}")
print(f"50% - 80% - {turfdata.num_sv_areas_50_80}")
print(f"25% - 50% - {turfdata.num_sv_areas_25_50}")

print_df(turfdata.df_regions,"df_regions")

print_df(turfdata.df_halfyear_regions,"df_halfyear_regions")

turfdata.df_halfyear_regions.to_excel("c:/temp/df_halfyear_regions.xlsx")
turfdata.df_regions.to_excel("c:/temp/df_regions.xlsx")

turfdata.create_top10s(file_list)
turfdata.count_unique_zones(file_list)
turfdata.count_unique_turfers()

print_df(turfdata.top10_takes_last_six_months,"top10_takes_last_six_months")

print_df(turfdata.num_zones_changed,"num_zones_changed")

# Create a PDF document with A4 size
doc = SimpleDocTemplate("turfrapport.pdf", pagesize=A4)

# Create content for the report
heading = Paragraph(f"Turfrapport {turfdata.turfname} {manad_lista[turfdata.manad-1]} {turfdata.artal}", style_title)

print(f" {turfdata.num_regions_total} - {turfdata.num_regions_total_prev} - {turfdata.num_regions_total_2prev}")

print("Test top 10")
print("===========")
print(turfdata.top10_zones_per_region_halfyear)
print("---")
print(turfdata.top10_zones_per_region_halfyear_prev)
print("---")
print(turfdata.top10_zones_per_region)
print("---")
print(turfdata.top10_zones_per_region_prev)

#print(turfdata.top10_takes_last_six_months.iloc[0])
#print(int((turfdata.top10_takes_last_six_months.iloc[0]).iloc[0]))
#introtext=create_introtext(turfdata)

turfdata.hotzones(file_list)

turfdata.shares(file_list)

intro_paragraph = Paragraph(create_introtext(turfdata), style_normal)

wardedfarger_heading = Paragraph("Wardedfärger", style_small_title)

warded_paragraph = Paragraph(create_wardedtext(turfdata), style_normal)

table_wardedfarger_data = [[index] + list(row) for index, row in turfdata.df_wardedfarger.iterrows()]
# Include the column names as the first row in the table data.
table_wardedfarger_data.insert(0, [''] + list(turfdata.df_wardedfarger.columns))

print("df_wardedfarger")
print(turfdata.df_wardedfarger)
print("")
print(table_wardedfarger_data)
print("")

table_wardedfarger = Table(table_wardedfarger_data)
# Apply style to the table
table_wardedfarger.setStyle(style)

plot_series(turfdata.df_count_takes_trans['2 - 10'],turfdata.df_count_takes_trans['11 - 20'],turfdata.df_count_takes_trans['21 - 50'], filename = '2till50.png', title='gula till röda', xlabel='halvår', ylabel='Besök')
diagram_2till50 = Image("2till50.png", width = 14*cm, height = 7 * cm)
plot_series(turfdata.df_count_takes_trans['51 - 100'],turfdata.df_count_takes_trans['101 - 250'], filename = '51till250.png', title='Ljuslila', xlabel='halvår', ylabel='Besök')
diagram_51till250 = Image("51till250.png", width = 14*cm, height = 7 * cm)
plot_stacked_area((turfdata.df_count_takes_trans['251 - 500'],turfdata.df_count_takes_trans['501 - 1000'],turfdata.df_count_takes_trans['1001 och mer']), filename = '251ochmer.png', title='Mörklila', xlabel='halvår', ylabel='Besök')
diagram_251ochmer = Image("251ochmer.png", width = 14*cm, height = 8 * cm)

halfyear_heading = Paragraph("Senaste 6 månadernas turfande", style_small_title)
halfyear_paragraph = Paragraph(create_halfyeartext(turfdata), style_normal)


table_period_now = periodtext_kort(turfdata.artal,turfdata.manad)
prevp_artal,prevp_manad = prev_period(turfdata.artal,turfdata.manad)
table_period_prev = periodtext_kort(prevp_artal,prevp_manad)
table_halfyear_data = [("Zon", table_period_now, table_period_prev)] + [[index] + list(row) for index, row in turfdata.top10_takes_last_six_months.iterrows()]
table_halfyear = Table(table_halfyear_data)
table_halfyear.setStyle(style_top10)

plot_series(turfdata.df_count_takes_trans['Nya'], filename = 'nyazoner.png', title='Nya unika zoner', xlabel='halvår', ylabel='Antal')
diagram_nyazoner = Image("nyazoner.png", width = 14*cm, height = 7 * cm)
new_paragraph = Paragraph(create_newtext(turfdata),style_normal)

table_new_data = [("Zon", "Besök")] + [(idx, val) for idx, val in turfdata.top10_takes_new.items()]
table_new = Table(table_new_data)
table_new.setStyle(style_top10)

total_paragraph = Paragraph(create_totaltext(turfdata),style_normal)

table_total_data = [("Zon", "Besök")] + [(idx, val) for idx, val in turfdata.top10_takes_total.items()]
table_total = Table(table_total_data)
table_total.setStyle(style_top10)

interkationer_heading = Paragraph("Interaktioner", style_small_title)
interkationer_paragraph = Paragraph(create_interactiontext(turfdata),style_normal)

regional_heading = Paragraph("Regionala data", style_small_title)
regional_paragraph = Paragraph(create_regionaltext(turfdata, file_list),style_normal)

plot_series(turfdata.df_turfdata_trans['uniqueturfers'], filename = 'unikaturfare.png', title='Unika turfare', xlabel='halvår', ylabel='Antal')
diagram_unikaturfare = Image("unikaturfare.png", width = 14*cm, height = 8 * cm)
plot_series(turfdata.df_turfdata_trans['uniqueassists'], filename = 'unikaassist.png', title='Unika assisterade turfare', xlabel='halvår', ylabel='Antal')
diagram_unikaassist = Image("unikaassist.png", width = 14*cm, height = 8 * cm)

# Build the report content
flowables = [heading, intro_paragraph, wardedfarger_heading, warded_paragraph, table_wardedfarger,
             diagram_2till50, diagram_51till250, diagram_251ochmer, interkationer_heading, interkationer_paragraph, diagram_unikaturfare, diagram_unikaassist, 
             regional_heading, regional_paragraph, halfyear_heading, halfyear_paragraph,
             table_halfyear, diagram_nyazoner, new_paragraph, table_new, total_paragraph, table_total]

# Set up the document and write the content
doc.build(flowables)
