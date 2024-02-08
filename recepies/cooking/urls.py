from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('suggest/', suggest_ingredient, name='suggest'),
    path('suggestions/', suggested_ingredients, name='suggestions'),
    path('suggestion/<int:request_id>/', suggestion, name='suggestion'),
    path('edit/<int:request_id>/', edit_suggestion, name='edit_request'),
    path('approve/<int:request_id>/', approve_request, name='approve_request'),
    path('reject/<int:request_id>/', reject_request, name='reject_request'),
    path('recipe/<slug:slug>/', get_recipe, name='recipe'),
    path('cook_recipe/<int:recipe_id>/', cook_recipe, name='cook_recipe'),
    path('show_recipes_without_product/<int:product_id>/', show_recipes_without_product,
         name='show_recipes_without_product'),
    path('add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>/<str:units>/', add_product_to_recipe,
         name='add_product_to_recipe'),
]
