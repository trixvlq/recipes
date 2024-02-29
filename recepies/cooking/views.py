from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Prefetch, Q

from users.forms import *
from users.models import UserRecipeReview
from .forms import SuggestionForm
from .models import *


def is_valid_units(units: str):
    valid_units = [unit[1].lower() for unit in RecipeIngredient.UNITS]
    return units.lower() in valid_units


def get_type(units: str):
    valid_units = [unit[1] for unit in RecipeIngredient.UNITS]
    index = valid_units.index(units)
    return RecipeIngredient.UNITS[index][0]


def index(request):
    recipes = Recipe.objects.select_related('dish_type')
    context = {
        'user': request.user,
        'recipes': recipes,
        'page_name': 'Все рецепты'
    }
    return render(request, 'cooking/index.html', context)


def get_recipe(request, slug):
    receipt = get_object_or_404(
        Recipe.objects.prefetch_related(
            Prefetch('detailed_ingredients',
                     queryset=RecipeIngredient.objects.select_related('ingredient')
                     ),
            Prefetch('reviews', queryset=UserRecipeReview.objects.all())
            ,
        ),
        slug=slug
    )
    form = RecipeReviewForm()
    context = {
        'recipe': receipt,
        'form': form,
    }

    return render(request, 'cooking/recipe_detailed.html', context)


def add_product_to_recipe(request, recipe_id, product_id, weight, units):
    receipt = get_object_or_404(Recipe, id=recipe_id)
    product = get_object_or_404(Ingredient, id=product_id)
    if not is_valid_units(units):
        return HttpResponse("Неправильные единицы измерения")
    try:
        ingredient = RecipeIngredient.objects.get(receipt=receipt, ingredient=product)
        ingredient.amount = weight
        ingredient.units = get_type(units)
        ingredient.save()
    except RecipeIngredient.DoesNotExist:
        RecipeIngredient.objects.create(receipt=receipt, ingredient=product, amount=weight, units=units)
    return redirect('home')


def cook_recipe(request, recipe_id):
    receipt = get_object_or_404(Recipe, id=recipe_id)
    receipt.usage += 1
    receipt.save()
    return redirect('recipe', slug=receipt.slug)

@login_required
def suggest_ingredient(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            return redirect('home')
    else:
        form = SuggestionForm()
        return render(request, 'Cooking/suggest.html', {'title': 'Создать мороженное', 'form': form})


def suggested_ingredients(request):
    suggestions = RequestIngredient.objects.all()
    context = {
        'suggestions': suggestions
    }
    return render(request, 'cooking/suggestions.html', context)


def edit_suggestion(request, request_id):
    suggestion_instance = RequestIngredient.objects.get(id=request_id)
    form = SuggestionForm(instance=suggestion_instance)
    if request.method == "POST":
        form = SuggestionForm(request.POST, request.FILES, instance=suggestion_instance)
        if form.is_valid():
            suggest = form.save(commit=False)
            if form.has_changed():
                suggest.edited = True
            suggest.save()
            return redirect('home')
    else:
        form = SuggestionForm(instance=suggestion_instance)
    return render(request, 'cooking/suggest.html', {'form': form})


def approve_request(request, request_id):
    ingredient_request = get_object_or_404(RequestIngredient, id=request_id)
    ingredient_request.accepted = True
    ingredient_request.is_active = False
    ingredient, created = Ingredient.objects.get_or_create(title=ingredient_request.title,
                                                           description=ingredient_request.description,
                                                           image=ingredient_request.image,
                                                           carbs=ingredient_request.carbs,
                                                           fats=ingredient_request.fats,
                                                           protein=ingredient_request.protein,
                                                           vegan=ingredient_request.vegan,
                                                           halal=ingredient_request.halal)
    ingredient_request.save()
    return redirect('suggestions')


def suggestion(request, request_id):
    suggestion = RequestIngredient.objects.get(id=request_id)
    context = {
        'suggestion': suggestion
    }
    return render(request, 'cooking/suggestion.html', context)


def reject_request(request, request_id):
    ingredient_request = get_object_or_404(RequestIngredient, id=request_id)
    ingredient_request.is_active = False
    ingredient_request.accepted = False
    ingredient_request.save()
    return redirect('view_requests')


def show_recipes_without_product(request, product_id):
    product = get_object_or_404(Ingredient, id=product_id)
    recepies = Recipe.objects.filter(~Q(ingredients=product))
    context = {'product': product, 'recipes': recepies}
    return render(request, 'cooking/alergic.html', context)
