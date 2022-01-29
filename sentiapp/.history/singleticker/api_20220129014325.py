

import json
from django.http import JsonResponse
import requests

# Create your views here.
from tweepy  import Stream, auth
from tweepy import OAuthHandler
import tweepy

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
