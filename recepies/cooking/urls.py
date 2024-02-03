from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('recipe/<slug:slug>/', get_recipe, name='recipe'),
    path('cook_recipe/<int:recipe_id>/', cook_recipe, name='cook_recipe'),
    path('show_recipes_without_product/<int:product_id>/', show_recipes_without_product, name='show_recipes_without_product'),
    path('add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>/<str:units>/', add_product_to_recipe, name='add_product_to_recipe'),
]
