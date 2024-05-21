def create_introtext(turfdata):

    introtext = f"{turfdata.turfname} har gjort totalt {turfdata.takes_total} takes i {turfdata.num_zones_total} unika zoner i {turfdata.num_regions_total} olika regioner. "
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

    return introtext

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
    