import tweepy
import pandas as pd
import os

pol = pd.read_csv(r"C:\Users\parth\OneDrive\Desktop\csv\politicians_3_30 - politicians_2_13 (2).csv")
dir = r'C:\Users\parth\OneDrive\Desktop\csv\raw_tweets'

api_key = r'YOUR_API_KEY'
api_key_secret = r'YOUR_API_KEY_SECRET'
bearer_token = r'YOUR_BEARER_TOKEN'
access_token = r'YOUR_ACCESS_TOKEN'
access_token_secret = r'YOUR_ACCESS_TOKEN_SECRET'

api = tweepy.Client(
 bearer_token,
 api_key,
 api_key_secret,
 access_token,
 access_token_secret,
 wait_on_rate_limit = True
 )

rel_pol = []
counts = []

def get_following_count(handle):
    return api.get_user(username = handle, user_fields='public_metrics').data.public_metrics['followers_count']#['public_metrics']#public_metrics.followers_count

for handle in os.listdir(dir):
    try:
        counts.append(get_following_count(handle))
    except:
        counts.append(0)
    
    rel_pol.append(handle)

rel_pol_df = pd.DataFrame({'Handle' : rel_pol,
                           'Follower Count' : counts})

rel_pol_df.to_csv(r'data\politicians_follower_count.csv')
