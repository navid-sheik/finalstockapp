from django.contrib import admin
from django.urls import path, include
from singleticker import views


urlpatterns = [
    path('dock/', views.test, name="another"),
   
    

]
