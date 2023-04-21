import pandas as pd
import json

# define file list and initialize a dictionary to store the data
file_list =['takes202210', 'takes202204', 'takes202110', 'takes202104','takes202010', 'takes202004', 'takes201910', 'takes201904','takes201810', 'takes201804', 'takes201710']
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
num_periods = len (file_list)

for i in range(num_periods-1):
    halfyear_col_name = file_list[i]+'halfyear'
    df[halfyear_col_name] = df[file_list[i]]-df[file_list[i+1]]

for i in range(num_periods-2):
    halfyear_col_name = file_list[i]+'year'
    df[halfyear_col_name] = df[file_list[i]]-df[file_list[i+2]]

# get top 10 takes totaly
top10_takes_totaly = df['takes202210'].nlargest(10).astype(int)

top10_zones = list(top10_takes_totaly.index)

print(df_total)

counts = {}
#for col in df_total.columns:
#    counts[col] ={
#            '2-20': ((df[col] 
#        }

# get top 10 takes last six months
top10_takes_last_six_months = df['takes202210halfyear'].nlargest(10).astype(int)
top10_takes_last_six_months_201804 = df['takes201804halfyear'].nlargest(10).astype(int)

# get top 10 takes last twelve months
#top10_takes_last_twelve_months = df['takes202210year'].nlargest(10).astype(int)


# print the two lists
print("Top 10 takes totaly:")
print(top10_takes_totaly)

print("\nTop 10 takes last six months:")
print(top10_takes_last_six_months)

#print("\nTop 10 takes last six months:")
#print(top10_takes_last_twelve_months)

print("\nTop 10 takes last six months (201804):")
print(top10_takes_last_six_months_201804)


print(df.loc['GultGuld'])
