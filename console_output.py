import pandas as pd
import json

def print_df(df, title):
    print(title)
    bar= '=' * len(title)
    print(bar)
    print(df)
    print("")
