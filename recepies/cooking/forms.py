from django.forms import ModelForm, forms
from .models import *


class SuggestionForm(ModelForm):
    class Meta:
        model = RequestIngredient
        fields = ['title', 'description', 'image', 'carbs', 'fats', 'protein', 'calories', 'vegan', 'halal']

