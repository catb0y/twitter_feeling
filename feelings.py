from vip import API_Key,API_Secret, Access_Token, Access_Token_Secret, App_ID, App_Key
import tweepy, codecs
from aylienapiclient import textapi
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import csv, io


# Twitter Credentials
auth = tweepy.OAuthHandler(API_Key, API_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

# Initialize a new client of AYLIEN Text API
client = textapi.Client(App_ID, App_Key)

# Search Hashtag and create text file
search_text = input("Tell me a search term and we will see how Twitter feels about it. ")
search_result = api.search(search_text, lang = "en", result_type = "recent", count = 100)  #better search! Tweepy
tweet_archive = codecs.open('tweet_archive.txt', 'w', 'utf-8')

for tweet in search_result:
    tweet_archive.write(tweet.text)
    tweet_archive.write("\n")

tweet_archive.close()
print("the tweets are alright")

# Analysis
# AYLIEN action, write csv
with io.open('twitter_feels.csv', 'w', encoding='utf8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Tweet", "Sentiment"])
    with io.open('tweet_archive.txt', 'r', encoding='utf8') as archive:
        for tweet in archive.readlines():
            # removing extra spaces
            tweet = tweet.strip()
            # remove empty tweets
            if len(tweet) == 0:
                continue

            # call to AYLIEN Text API
            sentiment = client.Sentiment({'text': tweet})
            # put results in csv file
            csv_writer.writerow([sentiment['text'], sentiment['polarity']])

# Open csv file
with io.open('twitter_feels.csv', 'r', encoding='utf8') as csvfile:
    # pandas reading the sentiment column
    df = pd.read_csv(csvfile)
    feels = df['Sentiment']

    # counter counts how many times each sentiment appears
    counter = Counter(feels)
    pos = counter['positive']
    neg = counter['negative']
    neut = counter['neutral']

# Plotting time
# Declaring variables
labels = 'Positive', 'Negative', 'Neutral'
sizes = [pos, neg, neutr]
colors = ['green', 'red', 'blue']

# Create a circle for the center of the plot (for donut purposes)
my_circle=plt.Circle( (0,0), 0.7, color='white')

# Create the actual pie
plt.pie(labels=labels, colors=colors, shadow=False)
plt.title("Twitter feelings for your search query: " + search_text )
plt.show()
