import tweepy
import configparser
import pandas as pd
import re

#create config file & read in personal keys
#read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# search tweets by keyword
keywords = 'N95'
limit=100

tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=100, tweet_mode='extended').items(limit)


# create DataFrame
columns = ['User', 'Tweet']
data = []

for tweet in tweets:
    data.append([tweet.user.screen_name, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

#clean tweets
def cleanTxt(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text)#removed @mentions
    text=re.sub(r'#','',text) #remove hashtag
    text=re.sub(r'RT[\s]+','',text) #remove RT
    text=re.sub(r'https?:\/\/\S+','',text)#remove hyperlink
    return text
df['Tweet']=df['Tweet'].apply(cleanTxt)

#save to csv file
df.to_csv('N95.csv')
print(df)
