from django.contrib import admin
from django.urls import path, include
from miner import views


urlpatterns = [
    path('stock/', views.test, name="test"),
   
    

]
