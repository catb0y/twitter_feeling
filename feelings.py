from vip import API_Key,API_Secret, Access_Token, Access_Token_Secret, App_ID, App_Key
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt
import tweepy, codecs
import pandas as pd
import csv, io


# Twitter Credentials
auth = tweepy.OAuthHandler(API_Key, API_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)


# Search Hashtag and create text file
search_text = input("Tell me a search term and we will see how Twitter feels about it. ")
search_result = api.search(search_text, lang = "en", result_type = "recent", count = 1000)  #better search! Tweepy
tweet_archive = codecs.open('tweet_archive.txt', 'w', 'utf-8')

for tweet in search_result:
    tweet_archive.write(tweet.text)
    tweet_archive.write("\n")

tweet_archive.close()
print("the tweets are alright")


# Analysis
# Write csv
with io.open('twitter_feels.csv', 'w', encoding='utf8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Tweet", "Sentiment"])
    with io.open('tweet_archive.txt', 'r', encoding='utf8') as archive:
        for tweet in archive.readlines():
            # removing extra spaces
            tweet = tweet.strip()
            # removing empty tweets
            if len(tweet) == 0:
                continue
            # TextBlob in action
            sentiment = TextBlob(tweet).sentiment.polarity
            # put results in csv file
            csv_writer.writerow([tweet, sentiment])

# Open csv file
with io.open('twitter_feels.csv', 'r', encoding='utf8') as csvfile:
    # pandas reading the file
    df = pd.read_csv(csvfile)
    print(df.head())

# THE PLOTS

# Plotting time - polarity graph
the_graph = df.plot(x="Tweet", y="Sentiment", title="Twitter feelings for your search query")
the_graph.set_xlabel("Tweet")
the_graph.set_ylabel("Polarity (positive/negative)")
plt.show()

# Plotting time - pie
pos = 0
neu = 0
neg = 0

for feeling in df["Sentiment"]:
    if feeling > 0.0:
        pos += 1
    elif feeling == 0.0:
        neu += 1
    else:
        neg += 1

labels = 'Positive', 'Negative', 'Neutral'
sizes = [pos, neg, neu]
colors = ['green', 'blue', 'red']

plt.pie(sizes, labels=labels, colors=colors)
plt.title("Twitter feelings for your search query")
plt.show()
