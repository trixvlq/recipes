from django.contrib import admin
from .models import *
from autoslug import AutoSlugField


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient


class RecipeStepInLine(admin.TabularInline):
    model = RecipeStep


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInLine, RecipeStepInLine]
    list_display = ('title', 'description', 'image')
    search_fields = ['title']
    exclude = ('usage', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(RecipeStep)
admin.site.register(RequestIngredient)
