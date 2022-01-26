from django.contrib import admin
from django.urls import path, include
from miner import views


urlpatterns = [
    path('single/', views.test, name="test"),
   
    

]
