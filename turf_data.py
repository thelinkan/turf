import pandas as pd

from format_data import import_data, takes_data

class TurfData:
    def __init__(self, turfname: str, artal: int, manad: int) -> None:
        self.turfname: str =turfname
        self.artal:int = artal
        self.manad:int = manad
        pass

    def import_main_dfs(self,file_list: list[str]) -> None:
        num_obs: int = len(file_list)
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

        print(self.df_takes_halfyear)

        self.df_since_last = self.df_takes_halfyear.drop(['Type'], axis=1)
        self.df_since_last["Senast"] =-1
        self.df_since_last["Senast2"] =-1

        halfyear_col_name = file_list[num_obs-1]+'halfyear'
        col_name = file_list[num_obs-1]
        self.df_since_last.loc[self.df_since_last[col_name] == 0, "Senast"] = -2
        self.df_since_last.loc[self.df_since_last[halfyear_col_name] > 0, "Senast"] = 0
        self.df_since_last.loc[self.df_since_last[halfyear_col_name] > 0, "Senast2"] = 0

        for i in range(1,num_obs-1):
            halfyear_col_name = file_list[num_obs-i-1]+'halfyear'
            col_name = file_list[num_obs-i-1]
            self.df_since_last.loc[(self.df_since_last[halfyear_col_name] > 0) & (self.df_since_last["Senast"] == -1), "Senast"] = i
            self.df_since_last.loc[(self.df_since_last[halfyear_col_name] > 0) & (self.df_since_last["Senast2"] == 0), "Senast2"] = i
            #print(f"{i} col_name {col_name}")

        #print(self.df_since_last[(self.df_since_last[file_list[num_obs-1]])==0])
        self.df_since_last.to_excel("c:/temp/df_since_last.xlsx")
        #for i in range(1,num_obs+1):
        #    print(file_list[num_obs-i])

    def set_df_count_takes(self ) -> None:
        
        self.df_count_takes = takes_data(self.df_takes.drop(['Country','Region','Area','Type','Takeovers'], axis=1))
        self.df_count_takes_trans = self.df_count_takes.transpose()
        self.df_count_takes_trans['Nya'] = self.df_count_takes_trans['Totalt'].diff(1)

        self.df_wardedfarger = self.df_count_takes.iloc[:,-6:]

    def count_unique_zones(self, file_list : list[str]) -> None:
        num_obs: int = len(file_list)
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

    def count_unique_turfers(self) -> None:
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
        

    def create_df_countries_regions(self, file_list: list[str]) -> None:
        num_obs: int = len(file_list)
        #dfa = self.df_takes.loc[self.df_takes[file_list[num_obs-1]]>0]
        dfa = self.df_takes_halfyear.loc[(self.df_takes['Country']!='None') & (self.df_takes['Country']!='se')]
        self.df_countries_off = pd.DataFrame.from_dict(dfa['Country'].value_counts())
        self.df_countries_off.rename(columns = {'count':'tot'}, inplace=True)
        for i in range(1,num_obs+1):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_countries_b = pd.DataFrame.from_dict(dfa['Country'].value_counts())
            df_countries_b.rename(columns = {'count':f'zones{file_list[i-1][5:]}'}, inplace=True)
            self.df_countries_off = self.df_countries_off.join(df_countries_b)

        self.df_countries_off = self.df_countries_off.fillna(0)
        self.num_countries_off = (self.df_countries_off[self.df_countries_off.columns[-1]] > 0).sum()
        self.num_zones_off = (self.df_countries_off[self.df_countries_off.columns[-1]].sum())

        dfa = self.df_takes_halfyear.loc[self.df_takes['Country']=='None']
        self.df_countries_nonoff = pd.DataFrame.from_dict(dfa['Region'].value_counts())
        for i in range(1,num_obs+1):
            dfa = self.df_takes.loc[self.df_takes[file_list[i-1]]>0]
            df_countries_nonoff_b = pd.DataFrame.from_dict(dfa['Region'].value_counts())
            df_countries_nonoff_b.rename(columns = {'count':f'zones{file_list[i-1][5:]}'}, inplace=True)
            self.df_countries_nonoff = self.df_countries_nonoff.join(df_countries_nonoff_b)
        
        self.df_countries_nonoff = self.df_countries_nonoff.fillna(0)
        self.num_countries_nonoff = (self.df_countries_nonoff[self.df_countries_nonoff.columns[-1]] > 0).sum()
        self.num_zones_nonoff = (self.df_countries_nonoff[self.df_countries_nonoff.columns[-1]].sum())

        


        #print("regioner och zoner utanför Sverige")
        #print(f"Länder: {self.num_countries_off} officiella och  {self.num_countries_nonoff} inofficiella - zoner: {self.num_zones_off} respektive {self.num_zones_nonoff}")
        #print(self.df_countries_nonoff)

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

    def hotzones(self, file_list: list[str]) -> None:
        num_obs: int = len(file_list)
        col_name = file_list[num_obs-1]
        halfyear_col_name = file_list[num_obs-1]+'halfyear'
        halfyear_col_name2 = file_list[num_obs-2]+'halfyear'
        halfyear_col_name3 = file_list[num_obs-3]+'halfyear'
        halfyear_col_name4 = file_list[num_obs-4]+'halfyear'
        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[halfyear_col_name] >= 50) & (self.df_takes_halfyear[halfyear_col_name2] >= 50) & (self.df_takes_halfyear[halfyear_col_name3] >= 50) & (self.df_takes_halfyear[halfyear_col_name4] >= 50)]
        self.num_hotzones = df_filtered.count()['Country']
        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[halfyear_col_name] >= 20) & (self.df_takes_halfyear[halfyear_col_name2] >= 20) & (self.df_takes_halfyear[halfyear_col_name3] >= 20) & (self.df_takes_halfyear[halfyear_col_name4] >= 20)]
        self.num_freqzones = df_filtered.count()['Country']
        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[halfyear_col_name] >= 5) & (self.df_takes_halfyear[halfyear_col_name2] >= 5) & (self.df_takes_halfyear[halfyear_col_name3] >= 5) & (self.df_takes_halfyear[halfyear_col_name4] >= 5)]
        self.num_regularzones = df_filtered.count()['Country']
        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[col_name] >= 101) & (self.df_takes_halfyear[halfyear_col_name] <= 1) & (self.df_takes_halfyear[halfyear_col_name2] <= 1) & (self.df_takes_halfyear[halfyear_col_name3] <= 1) & (self.df_takes_halfyear[halfyear_col_name4] <= 1)]
        self.num_coldzones = df_filtered.count()['Country']
        print(f"{self.num_hotzones} - {self.num_freqzones-self.num_hotzones} - {self.num_regularzones-self.num_freqzones} - {self.num_coldzones}")
        print(df_filtered)

    def create_top10s(self, file_list: list[str]) -> None:
        num_obs: int = len(file_list)

        df_filtered = self.df_takes_halfyear[(self.df_takes_halfyear[file_list[num_obs-2]] == 0) & (self.df_takes_halfyear.iloc[:, -1] > 0)][[self.df_takes_halfyear.columns[-2], self.df_takes_halfyear.columns[-1]]]
        df_filtered_prev = self.df_takes_halfyear[(self.df_takes_halfyear[file_list[num_obs-3]] == 0) & (self.df_takes_halfyear.iloc[:, -2] > 0)][[self.df_takes_halfyear.columns[-2], self.df_takes_halfyear.columns[-1]]]

        halfyear_col_name = file_list[num_obs-1]+'halfyear'
        halfyear_col_name_prev = file_list[num_obs-2]+'halfyear'
        col_name = file_list[num_obs-1]
        col_name_prev = file_list[num_obs-2]

        self.top10_takes_last_six_months = self.df_takes_halfyear[halfyear_col_name].nlargest(10).astype(int)
        self.top10_takes_total = self.df_takes[file_list[num_obs-1]].nlargest(10).astype(int)
        self.top10_takes_new = df_filtered[halfyear_col_name].nlargest(10).astype(int)
        self.num_newzones_green = df_filtered[df_filtered[halfyear_col_name]==1].count()[halfyear_col_name]
        self.num_newzones_prev = df_filtered_prev.count()[halfyear_col_name]
        self.num_newzones_prev_revisit = df_filtered_prev[df_filtered_prev[halfyear_col_name]>=1].count()[halfyear_col_name]
        #print(f"filtered for warded:\n new prev period:{self.num_newzones_prev}\n revisited this period: {self.num_newzones_prev_revisit}")
        print(f"filtered for warded:\n {df_filtered_prev[df_filtered_prev[halfyear_col_name]>=1]}")

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

    def shares(self, file_list: list[str]) -> None:
        num_obs:int = len(file_list)
        col_name = file_list[num_obs-1]
        df_takes_share = self.df_takes_halfyear[(self.df_takes_halfyear['Takeovers']>0)]
        df_takes_share['share'] = 100 * df_takes_share[col_name] / df_takes_share['Takeovers']
        df_takes_share = df_takes_share.sort_values(by=['share'], ascending = False)
        self.df_takes_share = df_takes_share[(df_takes_share['share'])>=5]
        self.num_zones_5percent = self.df_takes_share.count()['Country']
        df_takes_share = df_takes_share[(df_takes_share['share'])>=33]
        self.num_zones_33percent = df_takes_share.count()['Country']
        print(f"5: {self.num_zones_5percent} - 33: {self.num_zones_33percent}")
