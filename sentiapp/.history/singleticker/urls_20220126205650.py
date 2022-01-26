import imp
from django.contrib import admin
from django.urls import path, include
from singleticker import views
from singleticker.api import fetchStockData

app_name =  'singleticker'

urlpatterns = [
     path ('stock/<str:ticker_id>',views.singleStockView, name =  "single-stock" ),
     path('api/get_quote/<str:ticker_id>', fetchStockData, name="get_current_quote"),


   
    

]
