import pandas as pd
import time
import numpy as np
import os
import preprocessor as p
from googleapiclient import discovery

p.set_options(p.OPT.URL)

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey= r'AIzaSyAbiwMs2d3PfrkCrLd79V6bKnSw0qEjZmo',
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# assign directory
dir = r'C:\Users\parth\OneDrive\Desktop\csv\raw_tweets'

# iterate over files in
# that directory

for file in os.listdir(dir):
    i = 0
    f = os.path.join(dir, file)
    if os.path.isfile(f):
        user_df = pd.read_csv(f)

        # cleaned_text column represents the cleaned tweet if there's no retweet, or the cleaned
        # retweet text if the tweets is a retweet
        retweets = user_df[user_df['retweet_id'].notna()].drop('Unnamed: 0', axis = 1)
        not_retweets = user_df[user_df['retweet_id'].isna()].drop('Unnamed: 0', axis = 1)

        retweets['cleaned_text'] = retweets['tweet_text'].astype('str').apply(p.clean).str.replace(r'RT @[a-zA-Z0-9]*:', '', regex = True)
        not_retweets['cleaned_text'] = not_retweets['tweet_text'].astype('str').apply(p.clean)

        scores_df = pd.concat([retweets, not_retweets])

        text, tox, iden, ins, prof, thr = [], [], [], [], [], []
        for t in scores_df['cleaned_text']:
            time.sleep(0.7)
            print("'" + t[:20] + "'")
            analyze_request = {
            'comment': { 'text': t},
            'requestedAttributes': {'TOXICITY': {},
                                    'IDENTITY_ATTACK': {},
                                    'INSULT': {},
                                    'PROFANITY': {},
                                    'THREAT': {}
                                    }
            }

            try:
                response = client.comments().analyze(body=analyze_request).execute()

                text.append(t)
                tox.append(response['attributeScores']['TOXICITY']['summaryScore']['value'])
                iden.append(response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'])
                ins.append(response['attributeScores']['INSULT']['summaryScore']['value'])
                prof.append(response['attributeScores']['PROFANITY']['summaryScore']['value'])
                thr.append(response['attributeScores']['THREAT']['summaryScore']['value'])

                i += 1

            except:
                pass
            
            if i >= 500:
                break

        new_df = pd.DataFrame()
        new_df['text'] = t
        new_df['toxicity'] = tox
        new_df['identity_attack'] = iden
        new_df['insult'] = ins
        new_df['profanity'] = prof
        new_df['threat'] = thr

        new_df.to_csv(r'data\scored_tweets\' + file)
