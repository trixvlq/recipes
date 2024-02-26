from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from cooking.models import Recipe
from users.forms import RecipeReviewForm, CreateRecipe, IngredientFormSet
from users.models import UserRecipeReview


@login_required
def index(request):
    user = request.user
    recipes = Recipe.objects.select_related('dish_type').filter(user=user)
    context = {
        'user': user,
        'recipes': recipes
    }
    return render(request, 'users/cabinet.html', context)


@login_required
def list_recipies(request):
    user = request.user
    recipes = Recipe.objects.filter(user=user)
    context = {
        'recipes': recipes,
        'page_name': 'Рецепты пользователя'
    }
    return render(request, 'cooking/index.html', context)


@login_required
def review(request, slug):
    if request.method == "POST":
        form = RecipeReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            user = request.user
            review.user = user
            recipe = Recipe.objects.get(slug=slug)
            review.recipe = recipe
            if UserRecipeReview.objects.filter(user=user, recipe=recipe).exists():
                messages.add_message(request, messages.INFO, "You have already reviewed this recipe")
                return redirect('home')
            review.save()
            return redirect('home')
        else:
            return HttpResponse(form)


@login_required
def create_page(request):
    if request.method == "POST":
        recipe_form = CreateRecipe(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST)
        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            ingredient_formset.save()
            return redirect('home')
        else:
            for form in ingredient_formset:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
            return redirect('home')
    else:
        recipe_form = CreateRecipe()
        ingredient_formset = IngredientFormSet()
    return render(request, 'users/create_recipe.html', {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset})