from django.contrib import admin
from .models import *


class IngredientRecordsInLine(admin.TabularInline):
    model = IngredientRecords



admin.site.register(IngredientRecords)
admin.site.register(UserIngredientReview)
admin.site.register(UserRecipeReview)
