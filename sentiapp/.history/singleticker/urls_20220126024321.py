from django.contrib import admin
from django.urls import path, include
from singleticker import views


urlpatterns = [
    path ('background/',views.test, name =  "kami" )

   
    

]
