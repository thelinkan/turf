import pandas as pd
import json
import matplotlib.pyplot as plt
import os

def import_data(file_list):
    data_dict = {}
    turfdata_dict = {}
    alla_dict = {}

    # loop through each file and read the data
    for file in file_list:
        arman=file[5:11]
        file_changes=f"data/changes{arman}.json"
        file_turfdata=f"data/turfdata{arman}.json"
        file_allazoner = f"data/allzonesv5{arman}.json"

        #print(arman)
        with open(f"data/{file}.json") as f:
            data = json.load(f)
            counts = {f['properties']['title']: f['properties']['count'] for f in data['features']}
            data_dict[file] = counts
        # apply changes to zone names
        if(os.path.isfile(file_changes)):
            with open(file_changes) as f:
                changes = json.load(f)
                for feature in changes['features']:
                    for d in data_dict:
                        if(feature['properties']['old_name'] in data_dict[d]):
                            #print(f"old {d}: {data_dict[d][feature['properties']['old_name']]}")
                            data_dict[d][feature['properties']['new_name']] = data_dict[d][feature['properties']['old_name']]
                            del data_dict[d][feature['properties']['old_name']]
                            #print(f"new {d}: {data_dict[d][feature['properties']['new_name']]}")

        if(os.path.isfile(file_turfdata)):
            with open(file_turfdata) as f:
                turfdata = json.load(f)
                #print(turfdata)
                turfdata_dict[f"data{arman}"]=turfdata

        if(os.path.isfile(file_allazoner)):
            with open(file_allazoner, encoding='utf-8') as f:
                allazoner = json.load(f)
              
                alla_dict[f"period{arman}"]=allazoner

                #print(allazoner)

    zone_name_list=[]
    zone_takeovers_list=[]
    zone_country_list=[]
    zone_region_list=[]
    zone_area_list=[]
    zone_type_list=[]

    for z in alla_dict[f"period{arman}"]:
        zone_name = z['name']
        zone_takeovers = z['totalTakeovers']
        if 'region' in z:
            if 'area' in z['region']:
                zone_area = z['region']['area']['name']
            else:
                zone_area = "None"
            if 'country' in z['region']:
                zone_country = z['region']['country']
            else:
                zone_country = "None"
            zone_region = z['region']['name']
        else:
            zone_country = "None"
            zone_region = "None"
        if 'type' in z:
            zone_type = z['type']['name']
        else:
            zone_type = "None"
        zone_name_list.append(zone_name)
        zone_takeovers_list.append(zone_takeovers)
        zone_country_list.append(zone_country)
        zone_region_list.append(zone_region)
        zone_area_list.append(zone_area)
        zone_type_list.append(zone_type)
        #print(f"{zone_name} - {zone_takeovers} - {zone_country} - {zone_region}")
        
        

    df_alla = pd.DataFrame({'Zone':zone_name_list, 'Country': zone_country_list, 'Region': zone_region_list, 'Area': zone_area_list, 'Type': zone_type_list, 'Takeovers': zone_takeovers_list})
    
    
    #df_halfyear = df_halfyear.reset_index()
    #df_halfyear = df_halfyear.rename(columns={'index': 'Zone'})
    df_alla = df_alla.set_index('Zone')
    del zone_name_list, zone_country_list, zone_region_list, zone_takeovers_list, zone_area_list, zone_type_list

    #df_alla.to_excel("c:/temp/allazoner.xlsx")

    df_sverige = df_alla[(df_alla['Country']=='se')]
    df_sverige_areas = pd.DataFrame.from_dict(df_sverige['Area'].value_counts())
    df_sverige_areas.rename(columns = {'count':'Antal zoner'}, inplace=True)
    #df_sverige_areas.to_excel("c:/temp/sverigeareas.xlsx")


    # create pandas dataframe
    df = pd.DataFrame.from_dict(data_dict, orient='columns')
    df = df.fillna(0)
    df_allt = df.join(df_alla)
    df_allt.to_excel("c:/temp/takes.xlsx")

    df_zones = df_allt[['Country', 'Region', 'Area', 'Type', 'Takeovers']]
    df_zones.to_excel("c:/temp/zones.xlsx")

    df2 = pd.DataFrame.from_dict(turfdata_dict, orient='columns')
    #df2 = df2.fillna(0)

    #print(df2)

    return df_allt, df2, df_zones, df_sverige_areas
    
def takes_data(df):
    counts = {}
    for col in df.columns:
        df_tot_test = df[col]
        counts[col[5:]] = {
            '1': df_tot_test.loc[(df_tot_test == 1)].count(),
            '2 - 10': df_tot_test.loc[(df_tot_test > 1) & (df_tot_test <= 10)].count(),
            '11 - 20': df_tot_test.loc[(df_tot_test > 10) & (df_tot_test <= 20)].count(),
            '21 - 50': df_tot_test.loc[(df_tot_test > 20) & (df_tot_test <= 50)].count(),
            '51 - 100': df_tot_test.loc[(df_tot_test > 50) & (df_tot_test <= 100)].count(),
            '101 - 250': df_tot_test.loc[(df_tot_test > 100) & (df_tot_test <= 250)].count(),
            '251 - 500': df_tot_test.loc[(df_tot_test > 250) & (df_tot_test <= 500)].count(),
            '501 - 1000': df_tot_test.loc[(df_tot_test > 500) & (df_tot_test <= 1000)].count(),
            '1001 och mer': df_tot_test.loc[(df_tot_test > 1000)].count(),
            'Totalt': df_tot_test.loc[(df_tot_test > 0)].count()
        }
    df_counts = pd.DataFrame.from_dict(counts)
    
    return df_counts


def plot_series(*series, filename = 'file.png' , title='Line Plot', xlabel='X-axis', ylabel='Y-axis'):
    """
    Creates a line plot for each of the given series on the same figure.

    Parameters:
    *series (pandas.Series): Tuple of pandas.Series objects.
    title (str): Title for the plot.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    """
    # Create a line plot for each series
    for s in series:
        plt.plot(s, label=s.name)

    # Add title and axis labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    # Add legend
    plt.legend()
    plt.savefig(filename, dpi=300)
    plt.close()
    
    
    # Display the plot
    #plt.show()
    
    return plt
