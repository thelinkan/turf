import pandas as pd

from format_data import import_data, takes_data

class TurfData:
    def __init__(self, turfname) -> None:
        self.turfname=turfname
        pass

    def import_main_dfs(self,file_list):
        num_obs = len(file_list)
        self.df_takes, self.df_turfdata, self.df_zones, self.df_sverige_areas = import_data(file_list)

        self.df_turfdata_trans = self.df_turfdata.transpose()

        self.df_takes_halfyear = self.df_takes.drop(['Country','Region','Area','Type','Takeovers'], axis=1)
        self.df_takes_halfyear = self.df_takes_halfyear.reset_index()
        self.df_takes_halfyear = self.df_takes_halfyear.rename(columns={'index': 'Zone'})
        self.df_takes_halfyear = self.df_takes_halfyear.set_index('Zone')

        self.df_takes_halfyear = self.df_zones.join(self.df_takes_halfyear)

        for i in range(1,num_obs):
            halfyear_col_name = file_list[i]+'halfyear'
            self.df_takes_halfyear[halfyear_col_name] = self.df_takes_halfyear[file_list[i]]-self.df_takes_halfyear[file_list[i-1]]

        self.df_takes_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[file_list[num_obs-2]] == 0) & (self.df_takes_halfyear.iloc[:, -1] > 0)][[self.df_takes_halfyear.columns[-2], self.df_takes_halfyear.columns[-1]]]
        self.num_zones_total = (self.df_takes[self.df_takes.columns[-6]] > 0).sum()
        self.takes_total =  int(self.df_takes[self.df_takes.columns[-6]].sum())
        
        self.num_zones_halfyear = (self.df_takes_halfyear[self.df_takes_halfyear.columns[-1]] > 0).sum()
        self.takes_halfyear =  int(self.df_takes_halfyear[self.df_takes_halfyear.columns[-1]].sum())
        self.num_zones_newzones = (self.df_takes_filtered[self.df_takes_halfyear.columns[-1]] > 0).sum()
        self.takes_newzones = int(self.df_takes_filtered[self.df_takes_halfyear.columns[-1]].sum())


        
    def set_df_count_takes(self ):
        
        self.df_count_takes = takes_data(self.df_takes.drop(['Country','Region','Area','Type','Takeovers'], axis=1))
        self.df_count_takes_trans = self.df_count_takes.transpose()
        self.df_count_takes_trans['Nya'] = self.df_count_takes_trans['Totalt'].diff(1)

        self.df_wardedfarger = self.df_count_takes.iloc[:,-6:]

    def create_df_countries_regions(self,file_list):
        num_obs = len(file_list)

        dfa = self.df_takes.loc[self.df_takes[file_list[0]]>0]
        self.df_countries = pd.DataFrame.from_dict(dfa['Country'].value_counts())
        self.df_countries.rename(columns = {'count':file_list[0]}, inplace=True)
        for i in range(2,num_obs):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_countries_b = pd.DataFrame.from_dict(dfa['Country'].value_counts())
            df_countries_b.rename(columns = {'count':file_list[i-1]}, inplace=True)
            self.df_countries = self.df_countries.join(df_countries_b)

