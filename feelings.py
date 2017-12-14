#!/usr/bin/env python
from vip import *
from data import *
import tweepy
from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier


#Credentials
auth = tweepy.OAuthHandler(API_Key, API_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)


#Search Hashtag
search_text = raw_input("Tell me a search term and we will see how Twitter feels about it.")
search_result = api.search(search_text)  #better search!
analyze_this = ""
for item in search_result:
    analyze_this += item.text


#Analysis
cl = NaiveBayesClassifier(train)
print analyze_this
print cl.classify(analyze_this) #fix always neg
