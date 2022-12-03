import re
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import emoji


def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI)
    tweet = tweet.replace("#", "").replace("_", " ")
    return tweet


consumer_key = "G5khJLOqxrdTYDNnPz5VjtwMj"
consumer_secret = "TysJ0yjZbvqWuLkgBqmFo44tsgyZ2Prs9hYywcdLaZNR4o54ek"
access_token = "3402709913-tyJZo6rfoGmw9SgF5x1KhvwiUAgokPRbMleHSlf"
at_secret = "gvdy7ZYKm1OPlhel6Ir7V4R9UYpZj0pcmqVRpyoxhdrmi"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,at_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

search_term = input("Enter key or hashtag to search about: ")
key = search_term
search_term = search_term + "-filter:retweets"
numberOfTweets = int(input("Enter how many tweets to analyze: "))
timer = input("Please enter tweets from one day: 1 OR one week: 0 >>>")
if timer == "0":
    date = datetime.date(datetime.now()-timedelta(hours=168))
elif timer == "1":
    date = datetime.date(datetime.now()-timedelta(hours=24))
tweets = tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en', since=date).items(numberOfTweets)

positive = 0
negative = 0
polarity = 0
neutral = 0

df = pd.DataFrame([cleaner(tweet.full_text) for tweet in tweets],columns=['Tweets'])
scores_list = []

for tweet in df['Tweets']:
    analysis = TextBlob(tweet)
    scores_list.append(analysis.sentiment.polarity)
    polarity += analysis.sentiment.polarity

    if analysis.sentiment.polarity == 0:
        neutral += 1
    elif analysis.sentiment.polarity < 0:
        negative += 1
    elif analysis.sentiment.polarity > 0:
        positive += 1

result = "General thought about "+key+" is "
if polarity == 0:
    result += "Neutral"
elif polarity < 0:
    result += "Negative"
elif polarity > 0:
    result += "Positive"

print(result)

positive_p = (positive/numberOfTweets)*100
negative_p = (negative/numberOfTweets)*100
neutral_p = (neutral/numberOfTweets)*100

positive_p = format(positive_p,'.2f')
negative_p = format(negative_p,'.2f')
neutral_p = format(neutral_p,'.2f')

df['Sentiment'] = scores_list

df.to_excel(r'C:\Users\arif_\OneDrive\Masaüstü\Twitter.xlsx',index=False,header=True)


labels = ['Positive ['+str(positive_p)+'%]','Neutral ['+str(neutral_p)+'%]','Negative ['+str(negative_p)+'%]']
sizes = [positive_p, neutral_p, negative_p]
colors = ['yellowgreen','gray','red']
fig, ax = plt.subplots()
ax.pie(sizes,labels=labels,startangle=90,colors=colors)
plt.title("Analysis of news about "+search_term)
ax.axis('equal')

plt.show()


