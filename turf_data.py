import pandas as pd

from format_data import import_data, takes_data

class TurfData:
    def __init__(self, turfname, artal, manad) -> None:
        self.turfname=turfname
        self.artal = artal
        self.manad = manad
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

        self.df_filtered_2 = self.df_takes_halfyear[(self.df_takes[file_list[num_obs-7]] > 0) & (self.df_takes.iloc[:, -6] == 0)][[self.df_takes.columns[-7], self.df_takes.columns[-6]]]

        self.num_zones_changed = (self.df_filtered_2[self.df_filtered_2.columns[-2]] > 0).sum()
        self.takes_changed = int(self.df_filtered_2[self.df_filtered_2.columns[-1]].sum())
        self.takes_newzones = self.takes_newzones - self.takes_changed

        
    def set_df_count_takes(self ):
        
        self.df_count_takes = takes_data(self.df_takes.drop(['Country','Region','Area','Type','Takeovers'], axis=1))
        self.df_count_takes_trans = self.df_count_takes.transpose()
        self.df_count_takes_trans['Nya'] = self.df_count_takes_trans['Totalt'].diff(1)

        self.df_wardedfarger = self.df_count_takes.iloc[:,-6:]

    def count_unique_zones(self, file_list):
        num_obs = len(file_list)
        total_t0 = self.df_count_takes_trans['Totalt'].iloc[num_obs-1]
        gron_t0 =  self.df_count_takes_trans['1'].iloc[num_obs-1]
        gul_t0 =  self.df_count_takes_trans['2 - 10'].iloc[num_obs-1]
        orange_t0 = self.df_count_takes_trans['11 - 20'].iloc[num_obs-1]
        rod_t0 = self.df_count_takes_trans['21 - 50'].iloc[num_obs-1]

        total_t1 = self.df_count_takes_trans['Totalt'].iloc[num_obs-2]
        gron_t1 =  self.df_count_takes_trans['1'].iloc[num_obs-2]
        gul_t1 =  self.df_count_takes_trans['2 - 10'].iloc[num_obs-2]
        orange_t1 = self.df_count_takes_trans['11 - 20'].iloc[num_obs-2]
        rod_t1 = self.df_count_takes_trans['21 - 50'].iloc[num_obs-2]

        total_t2 = self.df_count_takes_trans['Totalt'].iloc[num_obs-3]
        gron_t2 =  self.df_count_takes_trans['1'].iloc[num_obs-3]
        gul_t2 =  self.df_count_takes_trans['2 - 10'].iloc[num_obs-3]
        orange_t2 = self.df_count_takes_trans['11 - 20'].iloc[num_obs-3]
        rod_t2 = self.df_count_takes_trans['21 - 50'].iloc[num_obs-3]

        total_t3 = self.df_count_takes_trans['Totalt'].iloc[num_obs-4]
        gron_t3 =  self.df_count_takes_trans['1'].iloc[num_obs-4]
        gul_t3 =  self.df_count_takes_trans['2 - 10'].iloc[num_obs-4]
        orange_t3 = self.df_count_takes_trans['11 - 20'].iloc[num_obs-4]
        rod_t3 = self.df_count_takes_trans['21 - 50'].iloc[num_obs-4]

        self.nya_unika_t0 = total_t0 - total_t1
        self.nya_unika_t1 = total_t1 - total_t2
        self.nya_unika_t2 = total_t2 - total_t3

    def count_unique_turfers(self, file_list):
        num_obs_turfdata = self.df_turfdata_trans.shape[0]

        self.unika_turfare_t0 = int(self.df_turfdata_trans['uniqueturfers'].iloc[num_obs_turfdata-1])
        self.unika_assist_t0 = int(self.df_turfdata_trans['uniqueassists'].iloc[num_obs_turfdata-1])
        self.ftt_t0 = int(self.df_turfdata_trans['ftt'].iloc[num_obs_turfdata-1])

        self.unika_turfare_t1 = int(self.df_turfdata_trans['uniqueturfers'].iloc[num_obs_turfdata-2])
        self.unika_assist_t1 = int(self.df_turfdata_trans['uniqueassists'].iloc[num_obs_turfdata-2])
        self.ftt_t1 = int(self.df_turfdata_trans['ftt'].iloc[num_obs_turfdata-2])

        self.unika_turfare_t2 = self.df_turfdata_trans['uniqueturfers'].iloc[num_obs_turfdata-3]
        self.unika_assist_t2 = self.df_turfdata_trans['uniqueassists'].iloc[num_obs_turfdata-3]
        self.ftt_t3 = int(self.df_turfdata_trans['ftt'].iloc[num_obs_turfdata-3])

        self.nya_turfare_t0 = self.unika_turfare_t0 - self.unika_turfare_t1
        self.nya_assist_t0 = self.unika_assist_t0 - self.unika_assist_t1
        self.nya_ftt_t0 = self.ftt_t0 - self.ftt_t1
        self.nya_turfare_t1 = self.unika_turfare_t1 - self.unika_turfare_t2
        self.nya_assist_t1 = self.unika_assist_t1 - self.unika_assist_t2
        

    def create_df_countries_regions(self,file_list):
        num_obs = len(file_list)

        dfa = self.df_takes.loc[self.df_takes[file_list[num_obs-1]]>0]
        self.df_countries = pd.DataFrame.from_dict(dfa['Country'].value_counts())
        self.df_countries.rename(columns = {'count':'tot'}, inplace=True)
        for i in range(1,num_obs):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_countries_b = pd.DataFrame.from_dict(dfa['Country'].value_counts())
            df_countries_b.rename(columns = {'count':file_list[i-1]}, inplace=True)
            self.df_countries = self.df_countries.join(df_countries_b)

        self.df_regions = pd.DataFrame.from_dict(self.df_takes['Region'].value_counts())
        self.df_regions.rename(columns = {'count':'Total'}, inplace=True)

        for i in range(1,num_obs+1):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_regions_b = pd.DataFrame.from_dict(dfa['Region'].value_counts())
            df_regions_b.rename(columns = {'count':f'zones{file_list[i-1][5:]}'}, inplace=True)
            self.df_regions = self.df_regions.join(df_regions_b)
        
        self.df_regions = self.df_regions.fillna(0)

        self.df_areas = pd.DataFrame.from_dict(self.df_takes['Area'].value_counts())
        self.df_areas.rename(columns = {'count':'Total'}, inplace=True)

        for i in range(1,num_obs+1):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_areas_b = pd.DataFrame.from_dict(dfa['Area'].value_counts())
            df_areas_b.rename(columns = {'count':f'zones{file_list[i-1][5:]}'}, inplace=True)
            self.df_areas = self.df_areas.join(df_areas_b)

        self.df_areas = self.df_areas.fillna(0)

        total_col_name = f'takes{file_list[num_obs-1][5:]}'
        self.df_sverige = self.df_takes[(self.df_takes[total_col_name] > 0)]
        self.df_sverige_areas_own = pd.DataFrame.from_dict(self.df_sverige['Area'].value_counts())
        self.df_sverige_areas_own.rename(columns = {'count':'Besökta zoner'}, inplace=True)
        self.df_sverige_areas = self.df_sverige_areas.join(self.df_sverige_areas_own)
        self.df_sverige_areas['Procent'] = (100 * self.df_sverige_areas['Besökta zoner']/self.df_sverige_areas['Antal zoner']).round(2)
        self.df_sverige_areas =self.df_sverige_areas.sort_values('Procent', ascending=False)

        self.num_sv_areas_100 = self.df_sverige_areas.loc[self.df_sverige_areas['Besökta zoner'] == self.df_sverige_areas['Antal zoner']].count()['Procent']
        self.num_sv_areas_80_100 = self.df_sverige_areas.loc[self.df_sverige_areas['Procent']>=80].count()['Procent']
        self.num_sv_areas_50_80 = self.df_sverige_areas.loc[self.df_sverige_areas['Procent']>=50].count()['Procent']
        self.num_sv_areas_25_50 = self.df_sverige_areas.loc[self.df_sverige_areas['Procent']>=25].count()['Procent']

        self.num_sv_areas_25_50 = self.num_sv_areas_25_50 - self.num_sv_areas_50_80
        self.num_sv_areas_50_80 = self.num_sv_areas_50_80 - self.num_sv_areas_80_100
        self.num_sv_areas_80_100 = self.num_sv_areas_80_100 - self.num_sv_areas_100

        self.df_halfyear_regions = self.df_regions
        self.df_halfyear_areas = self.df_areas
        for i in range(1,num_obs):
            total_col_name = f'zones{file_list[i][5:]}'
            total_col_name_prev = f'zones{file_list[i-1][5:]}'
            total_col_name_2prev = f'zones{file_list[i-2][5:]}'
            halfyear_col_name = f'zones{file_list[i][5:]}halfyear'
            self.df_halfyear_regions[halfyear_col_name] = self.df_halfyear_regions[total_col_name] - self.df_halfyear_regions[total_col_name_prev]
            self.df_halfyear_areas[halfyear_col_name] = self.df_halfyear_areas[total_col_name] - self.df_halfyear_areas[total_col_name_prev]

        self.num_regions_total = (self.df_regions[total_col_name] > 0).sum()
        self.num_regions_total_prev = (self.df_regions[total_col_name_prev] > 0).sum()
        self.num_regions_total_2prev = (self.df_regions[total_col_name_2prev] > 0).sum()
        self.num_regions_new = self.num_regions_total - self.num_regions_total_prev
        self.num_regions_2new = self.num_regions_total_prev - self.num_regions_total_2prev
        self.num_regions_halfyear = (self.df_halfyear_regions[self.df_halfyear_regions.columns[-1]] > 0).sum()
        self.num_regions_halfyear_prev = (self.df_halfyear_regions[self.df_halfyear_regions.columns[-2]] > 0).sum()

        self.num_areas_total = (self.df_areas[total_col_name] > 0).sum()
        self.num_areas_halfyear = (self.df_halfyear_areas[self.df_halfyear_areas.columns[-1]] > 0).sum()
        self.num_areas_halfyear_prev = (self.df_halfyear_areas[self.df_halfyear_areas.columns[-2]] > 0).sum()
    
    def create_top10s(self, file_list):
        num_obs = len(file_list)

        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[file_list[num_obs-2]] == 0) & (self.df_takes_halfyear.iloc[:, -1] > 0)][[self.df_takes_halfyear.columns[-2], self.df_takes_halfyear.columns[-1]]]

        halfyear_col_name = file_list[num_obs-1]+'halfyear'
        self.top10_takes_last_six_months = self.df_takes_halfyear[halfyear_col_name].nlargest(10).astype(int)
        self.top10_takes_total = self.df_takes[file_list[num_obs-1]].nlargest(10).astype(int)
        self.top10_takes_new = df_filtered[halfyear_col_name].nlargest(10).astype(int)

        halfyear_col_name_prev = file_list[num_obs-2]+'halfyear'
        self.top10_takes_last_six_months = pd.DataFrame(self.top10_takes_last_six_months).join(self.df_takes_halfyear[halfyear_col_name_prev])
        self.top10_takes_last_six_months = self.top10_takes_last_six_months.rename(columns={halfyear_col_name:file_list[num_obs-1][5:], halfyear_col_name_prev:file_list[num_obs-2][5:]})
        self.top10_takes_last_six_months = self.top10_takes_last_six_months.astype(int)

        col_name = 'zones'+file_list[num_obs-1][5:]
        halfyear_col_name = 'zones'+file_list[num_obs-1][5:]+'halfyear'
        df_halfyear_regions = self.df_halfyear_regions[self.df_halfyear_regions[halfyear_col_name]>0]
        self.top10_zones_per_region_halfyear = df_halfyear_regions[halfyear_col_name].nlargest(10).astype(int)
        self.top10_zones_per_region = self.df_regions[col_name].nlargest(10).astype(int)
        
        col_name_prev = 'zones'+file_list[num_obs-2][5:]
        halfyear_col_name_prev = 'zones'+file_list[num_obs-2][5:]+'halfyear'
        df_halfyear_regions = self.df_halfyear_regions[self.df_halfyear_regions[halfyear_col_name_prev]>0]
        self.top10_zones_per_region_halfyear_prev = df_halfyear_regions[halfyear_col_name_prev].nlargest(10).astype(int)
        self.top10_zones_per_region_prev = self.df_regions[col_name_prev].nlargest(10).astype(int)

