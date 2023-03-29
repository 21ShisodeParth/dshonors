import tweepy
import pandas as pd

users = pd.read_csv(r'data\politicians.csv")

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
 access_token_secret
 )

handles = users['Handle']

for h in handles:
   user_id = api.get_user(username = h).data.id
   tweet_ids = []
   tweet_texts = []
   usernames = []
   retweet_ids = []
   retweet_texts = []

   tweets = api.get_users_tweets(id = user_id, max_results = 100, expansions = ['referenced_tweets.id'])  ## this is how you access the data of the response object

   while True:

      for t in tweets.data:
         tweet_texts.append(t.text)
         tweet_ids.append(t.id)
         usernames.append(h)

         try:
            ref = t.referenced_tweets

            any_retweets = False

            for rt in ref:
               if rt.type == 'retweeted':
                  retweet_ids.append(rt.id)
                  retweet_texts.append(api.get_tweet(id = rt.id).data.text)
                  any_retweets = True
                  break
                  
            if any_retweets == False:
               retweet_ids.append(pd.NA)
               retweet_texts.append(pd.NA)
                  
         except:
            retweet_ids.append(pd.NA)
            retweet_texts.append(pd.NA)
      

      try:
         tweets = api.get_users_tweets(id = user_id,
                                       max_results = 100, 
                                       pagination_token = tweets.meta['next_token'])
         if not tweets.data:
            break
      except:
         break


   min_length = min(len(usernames), len(tweet_ids), len(tweet_texts), len(retweet_ids), len(retweet_texts))

   user_df = pd.DataFrame({'username' : usernames[:min_length],
                           'tweet_id' : tweet_ids[:min_length], 
                           'tweet_text' : tweet_texts[:min_length],
                           'retweet_id' : retweet_ids[:min_length],
                           'retweet_text' : retweet_texts[:min_length]})

   tweet_ids = []
   tweet_texts = []
   usernames = []
   retweet_ids = []
   retweet_texts = []

   user_df.to_csv(r'data\raw_tweets\' + h + r'.csv')
