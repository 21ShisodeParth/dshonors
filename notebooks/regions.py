import pandas as pd
import numpy as np
import os
from abb import us_state_to_abbrev, nickname_to_full, sen_cleaning

regions = pd.read_csv(r"data\politicians.csv")[['State', 'District', 'City']].drop_duplicates()

# Manual Addition of Missing Regions
regions.loc[len(regions.index)] = ['AR', 1, None]
regions.loc[len(regions.index)] = ['DC', 0, None]

regions[['Total Population',
         'Racial Diversity (Simpson Index)',
         'Foreign Born Proportion',
         'Median Income',
         'Mean Income', 
         'Median Age',
         'Bachelor\'s Degree or Higher Proportion', 
         'Unmployment Rate (%)']] = [None, None, None, None, None, None, None, None]

directory = r'C:\Users\parth\OneDrive\Desktop\csv\district_by_state'

abbrev_to_full = {us_state_to_abbrev[i] : i for i in us_state_to_abbrev} #REMOVE

def get_total_pop(rel_df):
    total = rel_df[(rel_df['Subject'] == 'Race') & (rel_df['Title'] == 'Total population')].iloc[0][2:]
    return total

def calc_simpson(rel_df):
    total = rel_df[(rel_df['Subject'] == 'Race') & (rel_df['Title'] == 'Total population')]
    breakdown = rel_df[(rel_df['Subject'] == 'Race') & (rel_df['Title'] != 'Total population') & (rel_df['Title'] != 'One race')]

    div_array = []

    for c in breakdown.columns[2:]:
        ratios = breakdown[c].astype(float) / float(total[c].iloc[0])
        div_array.append(1 - np.sum(ratios ** 2))

    #ratios = (breakdown['District 01 Estimate'].astype(float) / float(total['District 01 Estimate'].iloc[0])).values

    return div_array

def calc_foreign(rel_df):
    total = rel_df[(rel_df['Subject'] == 'Place of Birth') & (rel_df['Title'] == 'Total population')].iloc[0][2:]
    breakdown = rel_df[(rel_df['Subject'] == 'Place of Birth') & (rel_df['Title'] == 'Foreign born')].iloc[0][2:]

    prop_array = ((breakdown.astype(float)) / (total.astype(float))).values

    return prop_array

def get_income_med(rel_df):
    breakdown = rel_df[(rel_df['Subject'] == 'Income and Benefits (In 2021 inflation-adjusted dollars)') & (rel_df['Title'] == 'Median household income (dollars)')].iloc[0][2:].astype(float)
    return breakdown.values

def get_income_mean(rel_df):
    breakdown = rel_df[(rel_df['Subject'] == 'Income and Benefits (In 2021 inflation-adjusted dollars)') & (rel_df['Title'] == 'Mean household income (dollars)')].iloc[0][2:].astype(float)
    return breakdown.values

def get_age_med(rel_df):
    breakdown = rel_df[(rel_df['Subject'] == 'Sex and Age') & (rel_df['Title'] == 'Median age (years)')].iloc[0][2:].astype(float)
    return breakdown.values

def get_bach_prop(rel_df):
    breakdown = rel_df[(rel_df['Subject'] == 'Educational Attainment') & (rel_df['Title'] == 'Percent bachelor\'s degree or higher')].iloc[0][2:].astype(float) / 100
    return breakdown.values

def get_unem_prop(rel_df):
    breakdown = rel_df[(rel_df['Subject'] == 'Employment Status') & (rel_df['Title'] == 'Unemployment Rate')].iloc[0][2:].astype(float) / 100
    return breakdown.values

regions_raw = pd.DataFrame(columns = ['State', 
         'District', 
         'City',
         'Statistic Type', 
         'Statistic'])

#https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
for n in os.listdir(directory):
    f = os.path.join(directory, n)
    df = pd.read_csv(f)  
    
    rel_cols = ['Subject', 'Title'] + [c for c in df.columns if 'District' in c and 'Estimate' in c]

    rel_df = df[rel_cols].replace({',' : ''}, regex = True)

    state = us_state_to_abbrev[n[:n.find('_District')].replace('_', ' ')]
    print('\n' + state)  #REMOVE

    f_dict = { get_total_pop : 'Total Population',
               calc_simpson : 'Racial Diversity (Simpson Index)',
               calc_foreign : 'Foreign Born Proportion',
               get_income_med : 'Median Income', 
               get_income_mean : 'Mean Income',
               get_age_med : 'Median Age',
               get_bach_prop : 'Bachelor\'s Degree or Higher Proportion',
               get_unem_prop : 'Unmployment Rate (%)'}

    for f in f_dict:
        stats = f(rel_df)

        if len(stats) == 1:
            # Represents a congressional district "at-large"
            regions_raw.loc[len(regions_raw.index)] = [state, 0, None, f_dict[f], stats[0]]

        else:
            for i in range(len(stats)):
                # Represents iterating through multiple congressional districts
                regions_raw.loc[len(regions_raw.index)] = [state, i + 1, None, f_dict[f], stats[i]]


regions_states = regions_raw.groupby(by = ['State', 'Statistic Type'], sort = False).mean()
regions_states[['District', 'City']] = [None, None]

regions = pd.concat([regions_states.reset_index(), regions_raw])[['State', 'Statistic Type', 'Statistic', 'District', 'City']]

regions.reset_index().to_csv(r'data\regions.csv')
