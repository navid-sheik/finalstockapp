

import datetime
import imp
import json
import statistics
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests

# Create your views here.
from tweepy import Stream, auth
from tweepy import OAuthHandler
import tweepy
from home.models import TweetRecord, HourlyRecord, StockSummary

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
    url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/{timestamp}?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_quote': response})


def getHotTweet(request):

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets = 100

    keyword = 'Tesla #tesla'
    cursor = tweepy.Cursor(api.search_tweets, q=keyword,
                           tweet_mode="extended", result_type='recent', lang="en").items(1)

    searched_tweets = [status._json for status in cursor]
    json_string = [json.dumps(json_obj) for json_obj in searched_tweets]
    print("The json string")
    print(json_string)
    return JsonResponse({'tweet': json_string})


def getSentiment24Hours(request, ticker_id):
    stock = get_object_or_404(StockSummary, ticker=ticker_id)
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    records = HourlyRecord.objects.filter(
        stock=stock, tweet_date__gte=date_from)
    print("We have found this record  ",  records.count)

    fetched_date = datetime.datetime.now()
    list_stemmed = records.values_list('overall_stemmed_text', flat=True)
    wordcloud = stemmed_text_compress(list_stemmed)

    list_negative_count = records.values_list('negative_count', flat=True)
    negative_count_24_hours = sum(list_negative_count)

    list_positive_count = records.values_list('positive_count', flat=True)
    positive_count_24_hours = sum(list_positive_count)

    list_neutraul_count = records.values_list('neutraul_count', flat=True)
    neutraul_count_24_hours = sum(list_neutraul_count)

    total_tweets_count = negative_count_24_hours + \
        positive_count_24_hours + neutraul_count_24_hours

    list_negative = records.values_list('overall_neg', flat=True)
    mean_negative_24_hours = mean(list_negative)

    list_neutral = records.values_list('overall_neu', flat=True)
    mean_neutral_24_hours = mean(list_neutral)

    list_positive = records.values_list('overall_pos', flat=True)
    mean_positive_24_hours = mean(list_positive)

    list_compound = records.values_list('overall_compound', flat=True)
    mean_compound_24_hours = mean(list_compound)

    list_subjecivity = records.values_list('overall_subjectivity', flat=True)
    mean_subjectivity_24_hours = mean(list_subjecivity)

    list_polarity = records.values_list('overall_polarity', flat=True)
    mean_polarity_24_hours = mean(list_polarity)

    return JsonResponse({
        'fetched_date': fetched_date,
        'word_cloud_data': wordcloud,
        'negative_count': negative_count_24_hours,
        'positive_count': positive_count_24_hours,
        'neutral_count': negative_count_24_hours,
        'mean_negative': mean_negative_24_hours,
        'mean_positive':  mean_positive_24_hours,
        'mean_neutral':  mean_neutral_24_hours,
        'mean_polarity': mean_polarity_24_hours,
        'mean_subjectivity':  mean_subjectivity_24_hours,
        'mean_compound':  mean_compound_24_hours,
        'values_negatives':  list(list_negative),
        'values_positives':  list(list_positive),

        'values_neutral':  list(list_neutral),

        'values_compound':  list(list_compound),


        'values_polarity':  list(list_polarity),
        'values_subjectivity':  list(list_subjecivity),

    })


def mean(list_sentiment):
    return statistics.mean(list_sentiment)


# private method
def stemmed_text_compress(list):
    mytext = " "
    for obj in list:
        mytext += obj + " "
    return mytext
