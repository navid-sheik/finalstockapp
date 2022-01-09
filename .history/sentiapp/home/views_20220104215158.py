from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from tweepy  import Stream, auth
from tweepy import OAuthHandler
import tweepy

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
# from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

# import twitter_credentials
nltk.download('vader_lexicon')



ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET =  "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY =  "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"

def index(request):
    auth =  OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets  =  100
    tweets  =  []
    likes = []
    time = []
    keyword  = 'Tesla #tesla'
    cursor  =  tweepy.Cursor(api.search_tweets, q= keyword, tweet_mode="extended").items(number_of_tweets)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    for tweet in cursor:
        print(tweet.full_text)

        tweet_list.append(tweet.full_text)
        analysis = TextBlob(tweet.full_text)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.full_text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity
        
        if neg > pos:
            negative_list.append(tweet.full_text)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet.full_text)
            positive += 1
        
        elif pos == neg:
            neutral_list.append(tweet.full_text)
            neutral += 1

    # positive = percentage(positive, number_of_tweets)
    # negative = percentage(negative, number_of_tweets)
    # neutral = percentage(neutral, number_of_tweets)
    # polarity = percentage(polarity, number_of_tweets)
    # positive = format(positive, '.1f')
    # negative = format(negative, '.1f')
    # neutral = format(neutral, '.1f')


    #Number of Tweets (Total, Positive, Negative, Neutral)
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    print('total number: ',len(tweet_list))
    print('positive number: ',len(positive_list))
    print('negative number: ', len(negative_list))
    print('neutral number: ',len(neutral_list))

    print(tweet_list)


    context = {"tweets" : tweets, "navid" : "something"}
    return render(request, 'home/pages/home.html', context)
    