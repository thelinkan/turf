def create_introtext(turfdata):

    introtext = f"{turfdata.turfname} har gjort totalt {turfdata.takes_total} besök i {turfdata.num_zones_total} unika zoner i {turfdata.num_regions_total} olika regioner. "
    introtext = introtext + f"Under de senaste 6 månadernas turfande för {turfdata.turfname} var {turfdata.top10_takes_last_six_months.index.values[0]} "
    introtext = introtext + f"den vanligaste zonen med {int((turfdata.top10_takes_last_six_months.iloc[0]).iloc[0])} besök. "
    if(turfdata.top10_takes_last_six_months.index.values[0] == turfdata.top10_takes_total.index.values[0]):
        introtext = introtext + f" Även den totalt vanligaste zonen under turfkariären är {turfdata.top10_takes_total.index.values[0]} med "
        introtext = introtext + f"totalt {turfdata.top10_takes_total.iloc[0]} besök."
    else:
        introtext = introtext + f" Den totalt sett vanligaste zonen under turfkariären är {turfdata.top10_takes_total.index.values[0]} med "
        introtext = introtext + f"totalt {turfdata.top10_takes_total.iloc[0]} besök."
    introtext = introtext + f" Totalt togs {turfdata.nya_unika_t0} nya unika zoner under {periodtext(turfdata.artal,turfdata.manad)}, "
    introtext = introtext + f"jämfört med {turfdata.nya_unika_t1} under halvåret innan. "
    introtext = introtext + f" Den nya zon som togs flest gånger under halvåret var {turfdata.top10_takes_new.index.values[0]} "
    introtext = introtext + f"med {turfdata.top10_takes_new.iloc[0]} besök.\n\n"
    introtext = introtext + f" Totalt har zoner tagits från {turfdata.unika_turfare_t0} olika turfare, en ökning med {turfdata.nya_turfare_t0} under senaste halvåret.\n\n"
    introtext = introtext + f" {turfdata.num_hotzones} zoner är högtrafikszoner, dvs {turfdata.turfname} har tagit de zonerna minst 50 gånger varje halvår de senaste 4 halvåren. "
    introtext = introtext + f" Därutöver är {turfdata.num_freqzones} zoner frekvent besökta (minst 20 besök per halvår de senaste 4 halvåren, men inte högtrafikszon) v"
    introtext = introtext + f" och {turfdata.num_regularzones} zoner är besökta minst 5 gånger per halvår de senaste 4 halvåren, men inte frekvent eller högtrafik.\n\n"
    introtext = introtext + f" {turfdata.num_coldzones} zoner är kalla zoner. De har besökts minst 101 gånger var totalt, men de senaste 4 halvåren har det blivit som mest "
    introtext = introtext + f" ett besök varje halvår. \n\n"

    introtext = introtext.replace('\n','<br />\n')
    return introtext

def create_wardedtext(turfdata):
    wardedtext = "I detta avsnitt kommer information om hur många zoner som har respektive wardedfärg. "
    wardedtext = wardedtext + "Förutom de vanliga färgerna grön, gul, röd och lila, så har de lila zonerna delats upp i 51-100, 101-250, 251-500, 501-1000 och 1001+. "
    wardedtext = wardedtext + "Ibland kan antalet zoner i en grupp minska, det beror på att fler zoner har flyttats upp en nivå, än som har tillkommit i den aktuella nivån. "
    wardedtext = wardedtext + "\n\n"
    wardedtext = wardedtext.replace('\n','<br />\n')
    return wardedtext

def create_halfyeartext(turfdata):
    halfyeartext = f"Under de senaste 6 månadernas turfande gjordes totalt {turfdata.takes_halfyear} besök vid {turfdata.num_zones_halfyear} olika zoner i {turfdata.num_regions_halfyear} olika regioner och {turfdata.num_areas_halfyear} olika areor (motsvarande kommuner). "
    if turfdata.num_regions_new>0:
        if turfdata.num_regions_2new>0:
            halfyeartext = halfyeartext + f" {turfdata.num_regions_new} av dessa regioner var helt nya, jämfört med {turfdata.num_regions_2new} föregående halvår. "
        else:
            halfyeartext = halfyeartext + f" {turfdata.num_regions_new} av dessa regioner var helt nya. "
    else:
        if turfdata.num_regions_2new>0:
            halfyeartext = halfyeartext + f" Det var inga nya regioner det senaste halvåret, men {turfdata.num_regions_2new} var nya föregående halvår. "
    halfyeartext = halfyeartext + f"Av besöken detta halvår gjordes totalt {turfdata.takes_newzones} besök vid {turfdata.num_zones_newzones} nya zoner. "
    #halfyeartext = halfyeartext + f"Motsvarande halvår för ett år sedan var det {takes_newzones_prev2} besök vid {num_zones_newzones} nya zoner. "


    if turfdata.nya_ftt_t0>0:
        halfyeartext = halfyeartext + f" Du lyckades vara den första turfaren att ta {turfdata.nya_ftt_t0} zoner (så kallad ftt).\n\n "
    else:
        halfyeartext = halfyeartext + f" Du lyckades inte vara den första turfaren att ta några zoner det senaste halvåret. \n\n"

    if(turfdata.num_zones_changed>0):
        halfyeartext = halfyeartext + f"Antalet besök i de nya zonerna kan vara något överskattad, då {turfdata.num_zones_changed} zoner antingen har bytt "
        halfyeartext = halfyeartext + f"namn under det senaste halvåret eller tagits bort utan att det kunnat korrigeras för. \n\n"

    halfyeartext = halfyeartext + f"Tabellen nedan visar hur många gånger {turfdata.turfname} besökt var och en av de tio zoner som besökts mest under de senaste sex månaderna,"
    halfyeartext = halfyeartext + f"samt hur många besök som gjorts i respektive zon de föregående sex månaderna. \n\n"
    halfyeartext=halfyeartext.replace('\n','<br />\n')
    return halfyeartext

def create_newtext(turfdata):
    newtext = f"Under {periodtext(turfdata.artal,turfdata.manad)} har följande tio nya zoner tagits flest gånger. \n\n"
    return newtext

def create_totaltext(turfdata):
    totaltext = f"De 10 zoner som tagits mest totalt är"
    return totaltext

def create_interactiontext(turfdata):
    interaktionertext = f" Totalt har zoner tagits från {turfdata.unika_turfare_t0} olika turfare, varav {turfdata.nya_turfare_t0} "
    interaktionertext = interaktionertext + f"var nya unika turfare {periodtext(turfdata.artal,turfdata.manad)}."
    interaktionertext = interaktionertext + f" Under halvåret innan ökade antalet unika turfare med {int(turfdata.nya_turfare_t1)}."
    interaktionertext = interaktionertext + f" Antalet unika turfare som har assistats har ökat från {turfdata.unika_assist_t1} till {turfdata.unika_assist_t0}."
    return interaktionertext

def create_regionaltext(turfdata, file_list):
    num_obs = len(file_list)
    halfyear_col_name = 'zones'+file_list[num_obs-1][5:]+'halfyear'
    topregion = turfdata.top10_zones_per_region.index.values[0]
    topregion_zones = turfdata.top10_zones_per_region.iloc[0]
    df_topregion = turfdata.df_regions.filter(items=[topregion], axis=0)
    topregion_zones_halfyear = int(df_topregion[halfyear_col_name].iloc[0])
    regionaltext = f"Över hela turfkariären är {topregion} den region där {turfdata.turfname}  besökt flest unika zoner, "
    regionaltext = regionaltext + f"med {topregion_zones} stycken. "
    regionaltext = regionaltext + f"Det är en ökning med {topregion_zones_halfyear} nya unika zoner {periodtext(turfdata.artal,turfdata.manad)}. "
    if(topregion == turfdata.top10_zones_per_region_halfyear.index.values[0]):
        regionaltext = regionaltext +f" {topregion} är också den region där flest nya zoner har besökts under det senaste halvåret.\n\n"
    else:
        regionaltext = regionaltext + f"Den region där  flest nya zoner besökts under {periodtext(turfdata.artal,turfdata.manad)} var "
        regionaltext = regionaltext + f"{turfdata.top10_zones_per_region_halfyear.index.values[0]} där {turfdata.top10_zones_per_region_halfyear.iloc[0]} "
        regionaltext = regionaltext + f"nya unika zoner besöktes. \n\n"
    if(turfdata.num_sv_areas_100>0):
        if (turfdata.num_sv_areas_100 == 1):
            text_kommun = "kommun"
            text_svensk = "svensk"
        else:
            text_kommun = "kommuner"
            text_svensk = "svenska"
        if (turfdata.num_sv_areas_80_100 == 1):
            text_kommun_80 = "kommun"
        else:
            text_kommun_80 = "kommuner"
        regionaltext = regionaltext + f" {turfdata.turfname} har besökt alla zoner i {turfdata.num_sv_areas_100} {text_svensk} {text_kommun}."
        regionaltext = regionaltext + f" Därutöver har han besökt minst 80 procent av zonerna i {turfdata.num_sv_areas_80_100} {text_kommun_80} och " 
        regionaltext = regionaltext + f" minst 50 procent av zonerna (men mindre än 80 procent) i {turfdata.num_sv_areas_50_80} kommuner. \n\n" 
    else:
        if (turfdata.num_sv_areas_80_100 == 1):
            text_kommun = "kommun"
        else:
            text_kommun = "kommuner"
        regionaltext = regionaltext + f" {turfdata.turfname} har för näravarande inte besökt alla zoner i svensk någon kommun. " 
        regionaltext = regionaltext + f" Däremot har han besökt minst 80 procent av zonerna i {turfdata.num_sv_areas_80_100} {text_kommun}. " 
        regionaltext = regionaltext + f" Därutöver har han besökt minst 50 procent av zonerna (men mindre än 80 procent) i {turfdata.num_sv_areas_50_80} kommuner. \n\n" 

    regionaltext = regionaltext + f" {turfdata.turfname} har besökt totalt {turfdata.num_zones_off} zoner i {turfdata.num_countries_off} olika officiella turfländer, utanför Sverige. "
    regionaltext = regionaltext + f" Därutöver har totalt {turfdata.num_zones_nonoff} zoner besökts i {turfdata.num_countries_nonoff} olika inofficiella turfländer. "
     
    
    regionaltext = regionaltext.replace('\n','<br />\n')

    return regionaltext



def periodtext_kort(artal,manad):
    if manad == 4:
        return f"vinter {str(artal-2001)}/{str(artal-2000)}"
    else:
        return f"sommar {str(artal-2000)}"
    
def periodtext(artal,manad):
    if manad == 4:
        return f"vinterhalvåret {str(artal-1)}/{str(artal-2000)}"
    else:
        return f"sommarhalvåret {str(artal-2000)}"
    
def prev_period(artal,manad):
    if(manad==10):
        return artal,4
    if(manad==4):
        return artal-1,10
    return 0,0
    