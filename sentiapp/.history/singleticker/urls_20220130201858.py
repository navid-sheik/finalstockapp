import imp
from django.contrib import admin
from django.urls import path, include
from singleticker import views
from singleticker.api import fetchStockData, fetchStockDataHistory,getHotTweet,getSentiment24Hours

app_name =  'singleticker'

urlpatterns = [
     path ('stock/<str:ticker_id>',views.singleStockView, name =  "single-stock" ),
     path('api/get_quote/<str:ticker_id>', fetchStockData, name="get_current_quote"),
     path('api/get_quote/<str:ticker_id>/<str:timestamp>', fetchStockDataHistory, name="get_time_history"),
     path('api/get_hot_tweet', getHotTweet, name="get_hot_tweet"),
     path('api/get_sentiment_last_24_hours', getSentiment24Hours, name="get_24_hours_sentiment"),



   
    

]
