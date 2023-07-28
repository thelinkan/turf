import pandas as pd
import json
import matplotlib.pyplot as plt
import os

def import_data(file_list):
    data_dict = {}

    # loop through each file and read the data
    for file in file_list:
        with open(f"data/{file}.json") as f:
            data = json.load(f)
            counts = {f['properties']['title']: f['properties']['count'] for f in data['features']}
            data_dict[file] = counts

    # create pandas dataframe
    df = pd.DataFrame.from_dict(data_dict, orient='columns')
    df = df.fillna(0)

    # apply changes to zone names
    for file in os.listdir('data'):
        if file.startswith('changes') and file.endswith('.json'):
            with open(f"data/{file}") as f:
                changes = json.load(f)
                print(changes)
                for feature in changes['features']:
                    old_name = feature['properties']['old_name']
                    new_name = feature['properties']['new_name']
                    for col in df.columns:
                        if old_name in df.index:
                            df.rename(index={old_name: new_name}, inplace=True)

    return df
    
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
