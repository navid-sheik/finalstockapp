from django.contrib import admin
from django.urls import path, include
from singleticker import views


urlpatterns = [
     path ('stock/<str:ticker_id>',views.singleStockView, name =  "single-stock" )


   
    

]
