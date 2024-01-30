from django.contrib import admin
from .models import Receipt, ReceiptIngredient, Ingredient
from autoslug import AutoSlugField


class ReceiptIngredientInLine(admin.TabularInline):
    model = ReceiptIngredient


class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ReceiptIngredientInLine, ]
    list_display = ('title', 'description', 'process', 'image')
    search_fields = ['title']
    exclude = ('rating', 'usage')


admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(ReceiptIngredient)
admin.site.register(Ingredient)
