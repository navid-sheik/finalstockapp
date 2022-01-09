from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import langdetect

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
from .models import StockSummary, TweetRecord
import datetime
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
    cursor  =  tweepy.Cursor(api.search_tweets, q= keyword, tweet_mode="extended", lang="en").items(number_of_tweets)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    try:
        stockSummary = StockSummary.objects.get(ticker="TSL")
    except StockSummary.DoesNotExist:
        stockSummary  =  StockSummary(ticker="TSL", last_fetched = datetime.datetime.now())
        stockSummary.save()
    for tweet in cursor:
        print(tweet.full_text)
        print(cleanTweet(tweet.full_text))
        print(tweet.id_str)
        print(tweet.created_at)
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(tweet.full_text))
        print("The negative value is  ",  map_sentimet['neg'])
        

        tweet_record, created = TweetRecord.objects.update_or_create(
            stock=stockSummary, 
            tweet_id=tweet.id_str,
            tweet_date =  tweet.created_at ,
            raw_text =  tweet.full_text ,
            processed_text =  cleanTweet(tweet.full_text),
            polarity =   TextBlob(cleanTweet(tweet.full_text)).sentiment.polarity,
            sentiment =  map_sentimet['text_sentiment'],
            subjectivity =  TextBlob(cleanTweet(tweet.full_text)).sentiment.subjectivity,
            neg =  map_sentimet['neg'],
            neu =  map_sentimet['neu'],
            pos =  map_sentimet['pos'],
            compound  = map_sentimet['comp']


        )

        if created:
            print("Created record")
        else :
            print("Recrded")

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
    print("Before " +  str(len(tweet_list)))
    tweet_list = list(dict.fromkeys(tweet_list))
    print("AFter " +   str(len(tweet_list)))


    
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    print('total number: ',len(tweet_list))
    print('positive number: ',len(positive_list))
    print('negative number: ', len(negative_list))
    print('neutral number: ',len(neutral_list))

    print(tweet_list)

    # tweet_list.drop_duplicates(inplace = True)


 


    tw_list = pd.DataFrame(tweet_list)
    tw_list["text"] = tw_list[0]

    #Removing RT, Punctuation etc
    remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
    rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()
    print(tw_list.head(100))


    # tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    # for index, row in tw_list['text'].iteritems():
    #     score = SentimentIntensityAnalyzer().polarity_scores(row)
    #     neg = score['neg']
    #     neu = score['neu']
    #     pos = score['pos']
    #     comp = score['compound']
    #     if neg > pos:
    #         tw_list.loc[index, 'sentiment'] = "negative"
    #     elif pos > neg:
    #         tw_list.loc[index, 'sentiment'] = "positive"
    #     else:
    #         tw_list.loc[index, 'sentiment'] = "neutral"
    #     tw_list.loc[index, 'neg'] = neg
    #     tw_list.loc[index, 'neu'] = neu
    #     tw_list.loc[index, 'pos'] = pos
    #     tw_list.loc[index, 'compound'] = comp



    context = {"tweets" : tw_list.to_html(), "navid" : "something"}
    return render(request, 'home/pages/home.html', context)



def dropDuplicates (tweet_list):
    return

def cleanTweet(tweet):
     
  

    #remove placeholder video 
    # new_tweet =  re.sub(r'{link}', '', tweet)

    # new_tweet = re.sub(r"\[video\]", '', new_tweet)

    # #not letter , punction , emoji , hash , non  english 
    # new_tweet =  re.sub(r"[^a-z\s\(\-:\)\\\/\];='#]", '', new_tweet)


    #twitter mention 
    new_tweet =  re.sub(r'@mention', '', tweet)


    # it will remove the old style retweet text "RT"
    new_tweet = re.sub(r'^RT[\s]+', '', new_tweet)

    # it will remove hyperlinks
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', new_tweet)

    # it will remove hashtags. We have to be careful here not to remove 
    # the whole hashtag because text of hashtags contains huge information. 
    # only removing the hash # sign from the word
    new_tweet = re.sub(r'#', '', new_tweet)

    # it will remove single numeric terms in the tweet. 
    new_tweet = re.sub(r'[0-9]', '', new_tweet)


    new_tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",new_tweet)
    new_tweet =  new_tweet.lower()
 
    return new_tweet

def perfomSentimentAnalysis (tweet):
    tweet_sentiment  =  TextBlob(tweet).sentiment
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    sentiment  = ""
    if neg > pos:
        sentiment = "negative"
    elif pos > neg:
        sentiment = "positive"
    else:
        sentiment =  "neutral"

    sentiment  = {}
    sentiment["neg"] = neg
    sentiment["neu"] = neu
    sentiment["pos"] = pos
    sentiment["comp"] = comp
    sentiment["text_sentiment"] = sentiment

    return sentiment

