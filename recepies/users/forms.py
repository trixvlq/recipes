from django import forms
from django.contrib.auth.models import User

from cooking.models import Recipe, RecipeIngredient, RecipeStep
from .models import UserRecipeReview


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = UserRecipeReview
        fields = ('rating', 'content')


class CreateRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'dish_type', 'description', 'image', 'halal', 'vegan')


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'units', 'amount']


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['title', 'description', 'image']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)