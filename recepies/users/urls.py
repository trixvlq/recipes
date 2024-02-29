from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='cabinet'),
    path('recipes/', list_recipies, name='users_recipes'),
    path('submit_review/<slug:slug>/', review, name='submit_review'),
    path('create_recipe/', create_page, name='create_recipe'),
    path('create_recipe/<int:extra_ing>/<int:extra_steps>/', create_page, name='create_recipe_extra'),
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]
