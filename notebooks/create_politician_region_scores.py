import pandas as pd

reg = pd.read_csv(r"data\regions.csv")

scores = pd.read_csv(r"data\politician_avg_std.csv")

pol = pd.read_csv(r"data\politicians.csv")

for df in [reg, pol]:
    cit_ind = df[df['City'].notna()].index.values
    for ind in cit_ind:
        df.at[ind, 'District'] = pd.NA

pol_follower_ct = pd.read_csv(r"data\politicians_follower_count.csv")

pol_complete = pol.merge(pol_follower_ct, on = 'Handle')

pol_complete['District'] = pol_complete['District'].fillna(9999).astype('float')
reg['District'] = reg['District'].fillna(9999).astype('float')

pol_reg = pol_complete.merge(reg, on = ['State', 'District', 'City'])
pol_reg_scores = pol_reg.merge(scores, on = 'Handle')

pol_reg_scores.replace(to_replace = 9999, value = None).to_csv(r'data\politician_region_scores.csv')
