import imp
from django.contrib import admin
from django.urls import path, include
from home import views
from home.api import fetch_symbol, get_most_active, get_most_gainers, get_most_losers, startMining, getAllStockBeingMined, getBatchStockPrices, getBatchStockNews, get_iex_volume
from singleticker.views import singleStockView

app_name = 'home'
urlpatterns = [
    path('', views.home_page, name="home"),
    path('example/', views.example, name="example"),
    path('background/', views.test, name="background"),
    path('stock/<str:ticker_id>', singleStockView, name="single"),
    path('api/get_symbol/', fetch_symbol, name="fetch_symbols"),
    path('api/get_most_active/', get_most_active, name="get_most_active"),
    path('api/get_most_gainers/', get_most_gainers, name="get_most_gainers"),
    path('api/get_most_losers/', get_most_losers, name="get_most_losers"),
    path('api/get_most_iex_volume/', get_iex_volume, name="get_iex_volume"),
    path('api/start_mining_tweets/<str:ticker_id>',
         startMining, name="start_mining_tweets"),
    path('api/get_all_mining_tweets', getAllStockBeingMined,
         name="get_all_mining_tweets"),
    path('api/get_batch_stock_prices/<str:stocks>',
         getBatchStockPrices, name="get_batch_stock_prices"),
    path('api/get_batch_news/<str:stocks>',
         getBatchStockNews, name="get_batch_news"),



]