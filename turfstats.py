import pandas as pd
import json

# define file list and initialize a dictionary to store the data
file_list =['takes202210.json', 'takes202204.json', 'takes202110.json', 'takes202104.json','takes202010.json', 'takes202004.json', 'takes201910.json', 'takes201904.json','takes201810.json', 'takes201804.json', 'takes201710.json']
data_dict = {}

# loop through each file and read the data
for file in file_list:
    with open(f"data/{file}") as f:
        data = json.load(f)
        counts = {f['properties']['title']: f['properties']['count'] for f in data['features']}
        data_dict[file[:-5]] = counts

# create pandas dataframe
df = pd.DataFrame.from_dict(data_dict, orient='columns')
df = df.fillna(0)

# create new column
df['takes202210halfyear'] = df['takes202210'] - df['takes202204']
df['takes202104halfyear'] = df['takes202104'] - df['takes202110']
df['takes202110halfyear'] = df['takes202110'] - df['takes202104']
df['takes202004halfyear'] = df['takes202104'] - df['takes202010']
df['takes202010halfyear'] = df['takes202010'] - df['takes202004']
df['takes202004halfyear'] = df['takes202004'] - df['takes201910']
df['takes201910halfyear'] = df['takes201910'] - df['takes201904']
df['takes201904halfyear'] = df['takes201904'] - df['takes201810']
df['takes201810halfyear'] = df['takes201810'] - df['takes201804']
df['takes201804halfyear'] = df['takes201804'] - df['takes201710']

#for col in df.columns:
#    if 'takes' in col:
#        halfyear_col_name = col + 'halfyear'
#        df[halfyear_col_name] = df[col] - df[col.replace('202210', '202204')]



df['takes202210year'] = df['takes202210'] - df['takes202110']

# get top 10 takes totaly
top10_takes_totaly = df['takes202210'].nlargest(10).astype(int)

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


print(df.loc['MarinaZone'])
