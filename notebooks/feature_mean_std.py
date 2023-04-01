import os
import numpy as np
import pandas as pd

dir = r'C:\Users\parth\OneDrive\Desktop\csv\scored_tweets'
reg = r"C:\Users\parth\OneDrive\Desktop\csv\regions_complete.csv"

scores = pd.DataFrame()

users = []
tox_mean, iden_mean, ins_mean, prof_mean, thr_mean = [], [], [], [], []
tox_std, iden_std, ins_std, prof_std, thr_std = [], [], [], [], []

for file in os.listdir(dir):
    f = os.path.join(dir, file)

    user_df = pd.read_csv(f)

    users.append(file)
    tox_mean.append(np.mean(user_df['toxicity']))
    iden_mean.append(np.mean(user_df['identity_attack']))
    ins_mean.append(np.mean(user_df['insult']))
    prof_mean.append(np.mean(user_df['profanity']))
    thr_mean.append(np.mean(user_df['threat']))
    tox_std.append(np.std(user_df['toxicity']))
    iden_std.append(np.std(user_df['identity_attack']))
    ins_std.append(np.std(user_df['insult']))
    prof_std.append(np.std(user_df['profanity']))
    thr_std.append(np.std(user_df['threat']))

scores['Handle'] = users
scores['toxicity_mean'] = tox_mean
scores['identity_attack_mean'] = iden_mean
scores['insult_mean'] = ins_mean
scores['profanity_mean'] = prof_mean
scores['threat_mean'] = thr_mean
scores['toxicity_std'] = tox_std
scores['identity_attack_std'] = iden_std
scores['insult_std'] = ins_std
scores['profanity_std'] = prof_std
scores['threat_std'] = thr_std

pol = pd.read_csv(r"data\politicians.csv")

upd_pol = scores.merge(pol, how = 'outer', on = 'Handle').iloc[:, :11]

pol_reg = upd_pol.merge(reg, how = 'inner', on = ['State', 'District', 'City'])

upd_pol.to_csv(r'data\politician_avg_std.csv')
