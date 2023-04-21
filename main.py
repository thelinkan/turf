import pandas as pd
import json
import matplotlib.pyplot as plt
from format_data import import_data, takes_data, plot_series

file_list = ['takes201710', 'takes201804','takes201810', 'takes201904', 'takes201910', 'takes202004','takes202010', 'takes202104', 'takes202110', 'takes202204', 'takes202210']

df = import_data(file_list)
df_counts = takes_data(df)
print(df_counts)
df_counts_trans = df_counts.transpose()

plt1 = plot_series(df_counts_trans['1'],df_counts_trans['2 - 10'])
plt2 = plot_series(df_counts_trans['501 - 1000'],df_counts_trans['1001+'])

plt1.show()
plt2.show()
