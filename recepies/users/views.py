from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from cooking.models import Recipe, RecipeIngredient
from users.forms import *
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
def create_page(request, extra_ing=1, extra_steps=1):
    IngredientFormSet = formset_factory(RecipeIngredientForm, extra=extra_ing)
    RecipeStepFormSet = formset_factory(RecipeStepForm, extra=extra_steps)
    if request.method == "POST":
        recipe_form = CreateRecipe(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST)
        steps_formset = RecipeStepFormSet(request.POST)
        if recipe_form.is_valid() and ingredient_formset.is_valid() and steps_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            for ingredient in ingredient_formset:
                ingredient_recipe = ingredient.cleaned_data['ingredient']
                units = ingredient.cleaned_data['units']
                amount = ingredient.cleaned_data['amount']
                if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient_recipe).exists():
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient_recipe, units=units,
                                                    amount=amount)
                else:
                    messages.add_message(request, messages.INFO,
                                         f"Ingredient {ingredient_recipe} is already in {recipe}")
            step_num = 1
            for step in steps_formset:
                title = step.cleaned_data['title']
                description = step.cleaned_data['description']
                image = step.cleaned_data['image']
                RecipeStep.objects.create(recipe=recipe, title=title, description=description,
                                                image=image,number=step_num)
                step_num+=1
            return redirect('home')
        else:
            return redirect('home')
    else:
        recipe_form = CreateRecipe()
        ingredient_formset = IngredientFormSet()
        steps_formset = RecipeStepFormSet()
    return render(request, 'users/create_recipe.html',
                  {'recipe_form': recipe_form,
                   'ingredient_formset': ingredient_formset,
                   'steps_formset': steps_formset,
                   'extra_ing': extra_ing,
                   'extra_steps': extra_steps, })


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('error')
    else:
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'users/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return HttpResponse('error')
    else:
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
