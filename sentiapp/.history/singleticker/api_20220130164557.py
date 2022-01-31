

import datetime
import imp
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests

# Create your views here.
from tweepy  import Stream, auth
from tweepy import OAuthHandler
import tweepy
from home.models import  TweetRecord, HourlyRecord, StockSummary

ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET = "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY = "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"


def fetchStockData(request, ticker_id):
    stock_ticker = ticker_id.lower()
    url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url  =  f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'

    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_quote': response})




def fetchStockDataHistory(request, ticker_id, timestamp):
    stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    url  =  f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/{timestamp}?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_quote': response})

def getHotTweet(request):

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets = 100

    keyword  = 'Tesla #tesla'
    cursor  =  tweepy.Cursor(api.search_tweets, q= keyword, tweet_mode="extended", result_type='popular', lang="en").items(1)

    searched_tweets = [status._json for status  in cursor]
    json_string  =  [json.dumps(json_obj) for json_obj in searched_tweets]
    print("The json string")
    print(json_string)
    return JsonResponse({'tweet': json_string})


def getSentiment24Hours(request, ticker_id):
    stock =  get_object_or_404(StockSummary, ticker = ticker_id)
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    records  = HourlyRecord.objects.filter(stock = stock,tweet_date_gte = date_from )
    print("We have found this record  ",  records.count)
    list_stemmed=  records.values_list('overall_stemmed_text', flat=True)
    wordcloud  =  stemmed_text_compress(list_stemmed)
    list_negative=  records.values_list('overall_stemmed_text', flat=True)

    return




#private method 
def stemmed_text_compress(list):
    mytext  =  " "
    for obj in list:
        mytext += obj + " "
    return mytext