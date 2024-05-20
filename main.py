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

from format_data import takes_data, plot_series, plot_stacked_series
from console_output import print_df
from report_text import create_introtext
from turf_data import TurfData

turfname='TheLinkan'

turfdata = TurfData(turfname)
print(turfdata.turfname)

file_list = ['takes201610', 'takes201704','takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010', 'takes202104', 'takes202110', 'takes202204', 'takes202210', 'takes202304', 'takes202310', 'takes202404']
manad_lista = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
num_obs = len(file_list)
artal = file_list[num_obs-1][5:9]
artal_int = int(artal)
manad = int(file_list[num_obs-1][9:11])

if manad == 4:
    period_text = f"vinterhalvåret {str(artal_int-1)}/{artal[2:]}"
    table_period_now = f"vinter {str(artal_int-2001)}/{str(artal_int-2000)}"
    table_period_prev = f"sommar {str(artal_int-2001)}"

else:
    period_text = f"sommarhalvåret {artal}"

# Importera data 
turfdata.import_main_dfs(file_list)

pd.options.display.float_format = '{:,.0f}'.format

print_df(turfdata.df_takes,"Main df")

turfdata.set_df_count_takes()
print_df(turfdata.df_count_takes,"df_counts")

print_df(turfdata.df_count_takes_trans,"df_counts_trans - class")

turfdata.df_takes.to_excel("c:/temp/df.xlsx")

print_df(turfdata.df_takes_halfyear,"df_halfyear - class")

df_filtered = turfdata.df_takes_halfyear[(turfdata.df_takes_halfyear[file_list[num_obs-2]] == 0) & (turfdata.df_takes_halfyear.iloc[:, -1] > 0)][[turfdata.df_takes_halfyear.columns[-2], turfdata.df_takes_halfyear.columns[-1]]]

# Länder och regioner
turfdata.create_df_countries_regions(file_list)

print_df(turfdata.df_countries,"df_countries")

df_areas = pd.DataFrame.from_dict(turfdata.df_takes['Area'].value_counts())
df_areas.rename(columns = {'count':'Total'}, inplace=True)

for i in range(1,num_obs+1):
    dfa = turfdata.df_takes.loc[turfdata.df_takes[file_list[i-1]]>0]
    df_areas_b = pd.DataFrame.from_dict(dfa['Area'].value_counts())
    df_areas_b.rename(columns = {'count':f'zones{file_list[i-1][5:]}'}, inplace=True)
    df_areas = df_areas.join(df_areas_b)
    #print(f"{i}: {file_list[i-1]}")

df_areas = df_areas.fillna(0)

total_col_name = f'takes{file_list[num_obs-1][5:]}'
df_sverige = turfdata.df_takes[(turfdata.df_takes[total_col_name] > 0)]
df_sverige_areas_own = pd.DataFrame.from_dict(df_sverige['Area'].value_counts())
df_sverige_areas_own.rename(columns = {'count':'Besökta zoner'}, inplace=True)
df_sverige_areas = turfdata.df_sverige_areas.join(df_sverige_areas_own)
df_sverige_areas['Procent'] = (100 * df_sverige_areas['Besökta zoner']/df_sverige_areas['Antal zoner']).round(2)
df_sverige_areas =df_sverige_areas.sort_values('Procent', ascending=False)

num_sv_areas_100 = df_sverige_areas.loc[df_sverige_areas['Besökta zoner'] == df_sverige_areas['Antal zoner']].count()['Procent']
num_sv_areas_80_100 =df_sverige_areas.loc[df_sverige_areas['Procent']>=80].count()['Procent']
num_sv_areas_50_80 =df_sverige_areas.loc[df_sverige_areas['Procent']>=50].count()['Procent']
num_sv_areas_25_50 =df_sverige_areas.loc[df_sverige_areas['Procent']>=25].count()['Procent']

num_sv_areas_25_50 = num_sv_areas_25_50 - num_sv_areas_50_80
num_sv_areas_50_80 = num_sv_areas_50_80 - num_sv_areas_80_100
num_sv_areas_80_100 = num_sv_areas_80_100 - num_sv_areas_100

print_df(df_sverige_areas,"df_sverige_areas")

print(f"100% - {num_sv_areas_100}")
print(f"80% - 100% - {num_sv_areas_80_100}")
print(f"50% - 80% - {num_sv_areas_50_80}")
print(f"25% - 50% - {num_sv_areas_25_50}")

df_halfyear_regions = turfdata.df_regions
df_halfyear_areas = df_areas
for i in range(1,num_obs):
    total_col_name = f'zones{file_list[i][5:]}'
    total_col_name_prev = f'zones{file_list[i-1][5:]}'
    total_col_name_2prev = f'zones{file_list[i-2][5:]}'
    halfyear_col_name = f'zones{file_list[i][5:]}halfyear'
    df_halfyear_regions[halfyear_col_name] = df_halfyear_regions[total_col_name]-df_halfyear_regions[total_col_name_prev]
    df_halfyear_areas[halfyear_col_name] = df_halfyear_areas[total_col_name]-df_halfyear_areas[total_col_name_prev]

print_df(turfdata.df_regions,"df_regions")

print_df(df_halfyear_regions,"df_halfyear_regions")

df_halfyear_regions.to_excel("c:/temp/df_halfyear_regions.xlsx")
turfdata.df_regions.to_excel("c:/temp/df_regions.xlsx")
num_regions_total = (turfdata.df_regions[total_col_name] > 0).sum()
num_regions_total_prev = (turfdata.df_regions[total_col_name_prev] > 0).sum()
num_regions_total_2prev = (turfdata.df_regions[total_col_name_2prev] > 0).sum()
num_regions_new = num_regions_total - num_regions_total_prev
num_regions_2new = num_regions_total_prev - num_regions_total_2prev
num_regions_halfyear = (df_halfyear_regions[df_halfyear_regions.columns[-1]] > 0).sum()
num_regions_halfyear_prev = (df_halfyear_regions[df_halfyear_regions.columns[-2]] > 0).sum()

num_areas_total = (df_areas[total_col_name] > 0).sum()
num_areas_halfyear = (df_halfyear_areas[df_halfyear_areas.columns[-1]] > 0).sum()
num_areas_halfyear_prev = (df_halfyear_areas[df_halfyear_areas.columns[-2]] > 0).sum()


halfyear_col_name = file_list[num_obs-1]+'halfyear'
top10_takes_last_six_months = turfdata.df_takes_halfyear[halfyear_col_name].nlargest(10).astype(int)
#top10_takes_last_six_months = top10_takes_last_six_months.join(df_halfyear[total_col_name_prev])
top10_takes_total = turfdata.df_takes[file_list[num_obs-1]].nlargest(10).astype(int)
top10_takes_new = df_filtered[halfyear_col_name].nlargest(10).astype(int)

halfyear_col_name_prev = file_list[num_obs-2]+'halfyear'
top10_takes_last_six_months = pd.DataFrame(top10_takes_last_six_months).join(turfdata.df_takes_halfyear[halfyear_col_name_prev])
top10_takes_last_six_months = top10_takes_last_six_months.rename(columns={halfyear_col_name:file_list[num_obs-1][5:], halfyear_col_name_prev:file_list[num_obs-2][5:]})
print_df(top10_takes_last_six_months,"top10_takes_last_six_months")

print_df(turfdata.num_zones_changed,"num_zones_changed")

# Create a PDF document with A4 size
doc = SimpleDocTemplate("turfrapport.pdf", pagesize=A4)

# Set up styles
styles = getSampleStyleSheet()
style_title = styles['Title']
#style_bold = styles['Bold']
style_normal = styles['Normal']
style_small_title = styles['Heading2']


# Create content for the report
heading = Paragraph(f"Turfrapport {turfname} {manad_lista[manad-1]} {artal}", style_title)
zone_list = top10_takes_last_six_months.index.values
#print(zone_list)

#zone_list = list()
#if len(df[df['takes202210halfyear']==top10_takes_last_six_months[0]].index) > 0:
#    zone_name = df[df['takes202210halfyear']==top10_takes_last_six_months[0]].index[0]
#else:
#    zone_name = ""
total_t0 = turfdata.df_count_takes_trans['Totalt'][num_obs-1]
gron_t0 =  turfdata.df_count_takes_trans['1'][num_obs-1]
gul_t0 =  turfdata.df_count_takes_trans['2 - 10'][num_obs-1]
orange_t0 = turfdata.df_count_takes_trans['11 - 20'][num_obs-1]
rod_t0 = turfdata.df_count_takes_trans['21 - 50'][num_obs-1]

total_t1 = turfdata.df_count_takes_trans['Totalt'][num_obs-2]
gron_t1 =  turfdata.df_count_takes_trans['1'][num_obs-2]
gul_t1 =  turfdata.df_count_takes_trans['2 - 10'][num_obs-2]
orange_t1 = turfdata.df_count_takes_trans['11 - 20'][num_obs-2]
rod_t1 = turfdata.df_count_takes_trans['21 - 50'][num_obs-2]

total_t2 = turfdata.df_count_takes_trans['Totalt'][num_obs-3]
gron_t2 =  turfdata.df_count_takes_trans['1'][num_obs-3]
gul_t2 =  turfdata.df_count_takes_trans['2 - 10'][num_obs-3]
orange_t2 = turfdata.df_count_takes_trans['11 - 20'][num_obs-3]
rod_t2 = turfdata.df_count_takes_trans['21 - 50'][num_obs-3]

total_t3 = turfdata.df_count_takes_trans['Totalt'][num_obs-4]
gron_t3 =  turfdata.df_count_takes_trans['1'][num_obs-4]
gul_t3 =  turfdata.df_count_takes_trans['2 - 10'][num_obs-4]
orange_t3 = turfdata.df_count_takes_trans['11 - 20'][num_obs-4]
rod_t3 = turfdata.df_count_takes_trans['21 - 50'][num_obs-4]

nya_unika_t0 = total_t0 - total_t1
nya_unika_t1 = total_t1 - total_t2
nya_unika_t2 = total_t2 - total_t3

num_obs_turfdata = turfdata.df_turfdata_trans.shape[0]

unika_turfare_t0 = int(turfdata.df_turfdata_trans['uniqueturfers'][num_obs_turfdata-1])
unika_assist_t0 = int(turfdata.df_turfdata_trans['uniqueassists'][num_obs_turfdata-1])
ftt_t0 = int(turfdata.df_turfdata_trans['ftt'][num_obs_turfdata-1])

unika_turfare_t1 = int(turfdata.df_turfdata_trans['uniqueturfers'][num_obs_turfdata-2])
unika_assist_t1 = int(turfdata.df_turfdata_trans['uniqueassists'][num_obs_turfdata-2])
ftt_t1 = int(turfdata.df_turfdata_trans['ftt'][num_obs_turfdata-2])

unika_turfare_t2 = turfdata.df_turfdata_trans['uniqueturfers'][num_obs_turfdata-3]
unika_assist_t2 = turfdata.df_turfdata_trans['uniqueassists'][num_obs_turfdata-3]
ftt_t3 = int(turfdata.df_turfdata_trans['ftt'][num_obs_turfdata-3])

nya_turfare_t0 = unika_turfare_t0 - unika_turfare_t1
nya_assist_t0 = unika_assist_t0 - unika_assist_t1
nya_ftt_t0 = ftt_t0 - ftt_t1
nya_turfare_t1 = unika_turfare_t1 - unika_turfare_t2
nya_assist_t1 = unika_assist_t1 - unika_assist_t2

print(f" {num_regions_total} - {num_regions_total_prev} - {num_regions_total_2prev}")

print("Test top 10")
print("===========")
print(top10_takes_last_six_months)
print("---")
print(top10_takes_last_six_months.iloc[0])
print(int((top10_takes_last_six_months.iloc[0]).iloc[0]))
introtext=create_introtext(turfname, turfdata.takes_total, turfdata.num_zones_total, num_regions_total)
introtext = introtext + f"Under de senaste 6 månadernas turfande för {turfname} var {top10_takes_last_six_months.index.values[0]} den vanligaste zonen med {int((top10_takes_last_six_months.iloc[0]).iloc[0])} besök. "
if(top10_takes_last_six_months.index.values[0] == top10_takes_total.index.values[0]):
    introtext = introtext + f" Även den totalt vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
else:
    introtext = introtext + f" Den totalt sett vanligaste zonen under turfkariären är {top10_takes_total.index.values[0]} med totalt {top10_takes_total[0]} besök."
introtext = introtext + f" Totalt togs {nya_unika_t0} nya unika zoner under {period_text}, jämfört med {nya_unika_t1} under halvåret innan. "
introtext = introtext + f" Den nya zon som togs flest gånger under halvåret var {top10_takes_new.index.values[0]} med {top10_takes_new[0]} besök.\n\n"
introtext = introtext + f" Totalt har zoner tagits från {unika_turfare_t0} olika turfare, en ökning med {nya_turfare_t0} under senaste halvåret.\n\n"
if(num_sv_areas_100>0):
    if (num_sv_areas_100 == 1):
        text_kommun = "kommun"
        text_svensk = "svensk"
    else:
        text_kommun = "kommuner"
        text_svensk = "svenska"
    if (num_sv_areas_80_100 == 1):
        text_kommun_80 = "kommun"
    else:
        text_kommun_80 = "kommuner"
    introtext = introtext + f" {turfname} har besökt alla zoner i {num_sv_areas_100} {text_svensk} {text_kommun}."
    introtext = introtext + f" Därutöver har han besökt minst 80 procent av zonerna i {num_sv_areas_80_100} {text_kommun_80} och " 
    introtext = introtext + f" minst 50 procent av zonerna (men mindre än 80 procent) i {num_sv_areas_50_80} kommuner. " 
else:
    if (num_sv_areas_80_100 == 1):
        text_kommun = "kommun"
    else:
        text_kommun = "kommuner"
    introtext = introtext + f" {turfname} har för näravarande inte besökt alla zoner i svensk någon kommun. " 
    introtext = introtext + f" Däremot har han besökt minst 80 procent av zonerna i {num_sv_areas_80_100} {text_kommun}. " 
    introtext = introtext + f" Därutöver har han besökt minst 50 procent av zonerna (men mindre än 80 procent) i {num_sv_areas_50_80} kommuner. " 

introtext = introtext.replace('\n','<br />\n')

intro_paragraph = Paragraph(introtext, style_normal)

wardedfarger_heading = Paragraph("Wardedfärger", style_small_title)

wardedtext = "I detta avsnitt kommer information om hur många zoner som har respektive wardedfärg. "
wardedtext = wardedtext + "Förutom de vanliga färgerna grön, gul, röd och lila, så har de lila zonerna delats upp i 51-100, 101-250, 251-500, 501-1000 och 1001+. "
wardedtext = wardedtext + "Ibland kan antalet zoner i en grupp minska, det beror på att fler zoner har flyttats upp en nivå, än som har tillkommit i den aktuella nivån. "
wardedtext = wardedtext + "\n\n"
wardedtext = wardedtext.replace('\n','<br />\n')
warded_paragraph = Paragraph(wardedtext, style_normal)

#df_wardedfarger = turfdata.df_count_takes.iloc[:,-6:]
#table_wardedfarger_data = [list(df_wardedfarger.columns)] + [list(row) for row in df_wardedfarger.values]
#table_wardedfarger_data.insert(0, [''] + list(df_wardedfarger.rows))
table_wardedfarger_data = [[index] + list(row) for index, row in turfdata.df_wardedfarger.iterrows()]
# Include the column names as the first row in the table data.
table_wardedfarger_data.insert(0, [''] + list(turfdata.df_wardedfarger.columns))

print("df_wardedfarger")
print(turfdata.df_wardedfarger)
print("")
print(table_wardedfarger_data)
print("")

table_wardedfarger = Table(table_wardedfarger_data)
# Add style to the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
    ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
    ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, -1), (-1, -1), 10),
    ('TOPPADDING', (0, -1), (-1, -1), 6),
])

style_top10 = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
])

# Apply style to the table
table_wardedfarger.setStyle(style)

plot_series(turfdata.df_count_takes_trans['2 - 10'],turfdata.df_count_takes_trans['11 - 20'],turfdata.df_count_takes_trans['21 - 50'], filename = '2till50.png', title='gula till röda', xlabel='halvår', ylabel='Besök')
diagram_2till50 = Image("2till50.png", width = 14*cm, height = 7 * cm)
plot_series(turfdata.df_count_takes_trans['51 - 100'],turfdata.df_count_takes_trans['101 - 250'], filename = '51till250.png', title='Ljuslila', xlabel='halvår', ylabel='Besök')
diagram_51till250 = Image("51till250.png", width = 14*cm, height = 7 * cm)
plot_series(turfdata.df_count_takes_trans['251 - 500'],turfdata.df_count_takes_trans['501 - 1000'],turfdata.df_count_takes_trans['1001 och mer'], filename = '251ochmer.png', title='Mörklila', xlabel='halvår', ylabel='Besök')
diagram_251ochmer = Image("251ochmer.png", width = 14*cm, height = 8 * cm)

halfyear_heading = Paragraph("Senaste 6 månadernas turfande", style_small_title)

halfyeartext = f"Under de senaste 6 månadernas turfande gjordes totalt {turfdata.takes_halfyear} besök vid {turfdata.num_zones_halfyear} olika zoner i {num_regions_halfyear} olika regioner och {num_areas_halfyear} olika areor (motsvarande kommuner). "
if num_regions_new>0:
    if num_regions_2new>0:
        halfyeartext = halfyeartext + f" {num_regions_new} av dessa regioner var helt nya, jämfört med {num_regions_2new} föregående halvår. "
    else:
        halfyeartext = halfyeartext + f" {num_regions_new} av dessa regioner var helt nya. "
else:
    if num_regions_2new>0:
        halfyeartext = halfyeartext + f" Det var inga nya regioner det senaste halvåret, men {num_regions_2new} var nya föregående halvår. "
halfyeartext = halfyeartext + f"Av besöken detta halvår gjordes totalt {turfdata.takes_newzones} besök vid {turfdata.num_zones_newzones} nya zoner. "
#halfyeartext = halfyeartext + f"Motsvarande halvår för ett år sedan var det {takes_newzones_prev2} besök vid {num_zones_newzones} nya zoner. "


if nya_ftt_t0>0:
    halfyeartext = halfyeartext + f" Du lyckades vara den första turfaren att ta {nya_ftt_t0} zoner (så kallad ftt).\n\n "
else:
    halfyeartext = halfyeartext + f" Du lyckades inte vara den första turfaren att ta några zoner det senaste halvåret. \n\n"

if(turfdata.num_zones_changed>0):
    halfyeartext = halfyeartext + f"Antalet besök i de nya zonerna kan vara något överskattad, då {turfdata.num_zones_changed} zoner antingen har bytt "
    halfyeartext = halfyeartext + f"namn under det senaste halvåret eller tagits bort utan att det kunnat korrigeras för. \n\n"

halfyeartext = halfyeartext + f"Tabellen nedan visar hur många gånger {turfname} besökt var och en av de tio zoner som besökts mest under de senaste sex månaderna,"
halfyeartext = halfyeartext + f"samt hur många besök som gjorts i respektive zon de föregående sex månaderna. \n\n"
halfyeartext=halfyeartext.replace('\n','<br />\n')
halfyear_paragraph = Paragraph(halfyeartext, style_normal)


table_halfyear_data = [("Zon", table_period_now, table_period_prev)] + [[index] + list(row) for index, row in top10_takes_last_six_months.iterrows()]
table_halfyear = Table(table_halfyear_data)
table_halfyear.setStyle(style_top10)

plot_series(turfdata.df_count_takes_trans['Nya'], filename = 'nyazoner.png', title='Nya unika zoner', xlabel='halvår', ylabel='Antal')
diagram_nyazoner = Image("nyazoner.png", width = 14*cm, height = 7 * cm)


newtext = f"Under de senaste sex månaderna har följande tio nya zoner tagits flest gånger. \n\n"
new_paragraph = Paragraph(newtext,style_normal)

table_new_data = [("Zon", "Besök")] + [(idx, val) for idx, val in top10_takes_new.items()]
table_new = Table(table_new_data)
table_new.setStyle(style_top10)


totaltext = f"De 10 zoner som tagits mest totalt är"
total_paragraph = Paragraph(totaltext,style_normal)

table_total_data = [("Zon", "Besök")] + [(idx, val) for idx, val in top10_takes_total.items()]
table_total = Table(table_total_data)
table_total.setStyle(style_top10)

interkationer_heading = Paragraph("Interaktioner", style_small_title)

interaktionertext = f" Totalt har zoner tagits från {unika_turfare_t0} olika turfare, varav {nya_turfare_t0} var nya unika turfare {period_text}."
interaktionertext = interaktionertext + f" Under halvåret innan ökade antalet unika turfare med {nya_turfare_t1}."
interaktionertext = interaktionertext + f" Antalet unika turfare som har assistats har ökat från {unika_assist_t1} till {unika_assist_t0}."

interkationer_paragraph = Paragraph(interaktionertext,style_normal)

plot_series(turfdata.df_turfdata_trans['uniqueturfers'], filename = 'unikaturfare.png', title='Unika turfare', xlabel='halvår', ylabel='Antal')
unikaturfare = Image("unikaturfare.png", width = 14*cm, height = 8 * cm)
plot_series(turfdata.df_turfdata_trans['uniqueassists'], filename = 'unikaassist.png', title='Unika assisterade turfare', xlabel='halvår', ylabel='Antal')
unikaassist = Image("unikaassist.png", width = 14*cm, height = 8 * cm)

# Build the report content
flowables = [heading, intro_paragraph, wardedfarger_heading, warded_paragraph, table_wardedfarger,
             diagram_2till50, diagram_51till250, diagram_251ochmer, interkationer_heading, interkationer_paragraph, unikaturfare, unikaassist, halfyear_heading, halfyear_paragraph,
             table_halfyear, diagram_nyazoner, new_paragraph, table_new, total_paragraph, table_total]

# Set up the document and write the content
doc.build(flowables)


#plt2 = plot_series(df_counts_trans['501 - 1000'],df_counts_trans['1001+'])

#plt1.show()
#plt2.show()
