from django.forms import ModelForm

from cooking.models import Recipe, RecipeIngredient
from .models import UserRecipeReview


class RecipeReviewForm(ModelForm):
    class Meta:
        model = UserRecipeReview
        fields = ('rating', 'content')


class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'dish_type', 'description', 'image', 'halal', 'vegan')

class RecipeIngredientForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'units', 'amount']
