import pandas as pd
import json
import matplotlib.pyplot as plt

# define file list and initialize a dictionary to store the data
file_list = ['takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010', 'takes202104', 'takes202110', 'takes202204', 'takes202210']
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
df_total = df

#df_total_index = pd.to_datetime(df.index.str[5:], format='%Y%m')
# create new column
# get top 10 takes totaly
top10_takes_totaly = df['takes202210'].nlargest(10).astype(int)
top10_takes_totaly_201710 = df['takes201710'].nlargest(10).astype(int)

top10_zones = list(top10_takes_totaly.index)

#print(df_total)

counts = {}
for col in df_total.columns:
    df_tot_test = df_total[col]
    counts[col[5:]] = {
        '1': df_tot_test.loc[(df_tot_test == 1)].count(),
        '2 - 10': df_tot_test.loc[(df_tot_test > 1) & (df_tot_test <= 10)].count(),
        '11 - 20': df_tot_test.loc[(df_tot_test > 10) & (df_tot_test <= 20)].count(),
        '21 - 50': df_tot_test.loc[(df_tot_test > 20) & (df_tot_test <= 50)].count(),
        '51 - 100': df_tot_test.loc[(df_tot_test > 50) & (df_tot_test <= 100)].count(),
        '101 - 250': df_tot_test.loc[(df_tot_test > 100) & (df_tot_test <= 250)].count(),
        '251 - 500': df_tot_test.loc[(df_tot_test > 250) & (df_tot_test <= 500)].count(),
        '501 - 1000': df_tot_test.loc[(df_tot_test > 500) & (df_tot_test <= 1000)].count(),
        '1001+': df_tot_test.loc[(df_tot_test > 1000)].count(),
        'Totalt': df_tot_test.loc[(df_tot_test > 0)].count()
    }
df_counts = pd.DataFrame.from_dict(counts)
print(df_counts)

df_counts_trans = df_counts.transpose()
print(df_counts_trans)

#df_counts_trans.index = pd.to_datetime(df_counts_trans.index, format='%Y%m')
#half_year_periods = pd.PeriodIndex(df_counts_trans.index, freq='6M')
#df_half_year.index = half_year_periods
#df_half_year.columns = [col for col in df_half_year.columns]

# Extract the series 1, 2-10 and 11-20 from df_counts_trans
series1 = df_counts_trans.loc[:, '1']
series2_10 = df_counts_trans.loc[:, '2 - 10']
series11_20 = df_counts_trans.loc[:, '11 - 20']

# Create a line plot
plt.plot(series1, label='Series 1')
plt.plot(series2_10, label='Series 2-10')
plt.plot(series11_20, label='Series 11-20')

# Add title and axis labels
plt.title('Series 1, 2-10 and 11-20')
plt.xlabel('Year')
plt.ylabel('Count')

plt.xticks(rotation=90)

# Add legend
plt.legend()

# Display the plot
plt.show()

#print(df_half_year)

num_periods = len (file_list)

for i in range(1,num_periods):
    halfyear_col_name = file_list[i]+'halfyear'
    df[halfyear_col_name] = df[file_list[i]]-df[file_list[i-1]]


# get top 10 takes last six months
top10_takes_last_six_months = df['takes202210halfyear'].nlargest(10).astype(int)
top10_takes_last_six_months_201804 = df['takes201804halfyear'].nlargest(10).astype(int)

# get top 10 takes last twelve months
#top10_takes_last_twelve_months = df['takes202210year'].nlargest(10).astype(int)


# print the two lists
print("Top 10 takes totaly:")
print(top10_takes_totaly)
print(top10_takes_totaly_201710)

print("\nTop 10 takes last six months:")
print(top10_takes_last_six_months)

#print("\nTop 10 takes last six months:")
#print(top10_takes_last_twelve_months)

print("\nTop 10 takes last six months (201804):")
print(top10_takes_last_six_months_201804)


print(df_total.loc['GultGuld'])
