from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='cabinet'),
    path('recipes/', list_recipies, name='users_recipes'),
    path('submit_review/<slug:slug>/', review, name='submit_review'),
    path('create_recipe/', create_page, name='create_recipe'),
]
