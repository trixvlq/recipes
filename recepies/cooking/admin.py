from django.contrib import admin
from .models import Recipe, RecipeIngredient, Ingredient
from autoslug import AutoSlugField


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInLine, ]
    list_display = ('title', 'description', 'process', 'image')
    search_fields = ['title']
    exclude = ('rating', 'usage')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
