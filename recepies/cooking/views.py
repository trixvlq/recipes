from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Prefetch, Q
from .models import *


def is_valid_units(units: str):
    valid_units = [unit[1].lower() for unit in ReceiptIngredient.UNITS]
    return units.lower() in valid_units


def get_type(units: str):
    valid_units = [unit[1] for unit in ReceiptIngredient.UNITS]
    index = valid_units.index(units)
    return ReceiptIngredient.UNITS[index][0]


def index(request):
    recepies = Receipt.objects.all()
    context = {'recipes': recepies}
    return render(request, 'cooking/index.html', context)


def get_receipt(request, slug):
    receipt = get_object_or_404(Receipt.objects.prefetch_related(
        Prefetch('detailed_ingredients', queryset=ReceiptIngredient.objects.select_related('ingredient').all())),
        slug=slug)
    context = {'recipe': receipt}
    return render(request, 'cooking/receipt_detail.html', context)


def add_product_to_recipe(request, recipe_id, product_id, weight, units):
    receipt = get_object_or_404(Receipt, id=recipe_id)
    product = get_object_or_404(Ingredient, id=product_id)
    if not is_valid_units(units):
        return HttpResponse("Неправильные единицы измерения")
    try:
        ingredient = ReceiptIngredient.objects.get(receipt=receipt, ingredient=product)
        ingredient.amount = weight
        ingredient.units = get_type(units)
        ingredient.save()
    except ReceiptIngredient.DoesNotExist:
        ReceiptIngredient.objects.create(receipt=receipt, ingredient=product, amount=weight, units=units)
    return redirect('home')


def cook_recipe(request, recipe_id):
    receipt = get_object_or_404(Receipt, id=recipe_id)
    receipt.usage += 1
    receipt.save()
    return redirect('receipt', slug=receipt.slug)


def show_recipes_without_product(request, product_id):
    product = get_object_or_404(Ingredient, id=product_id)
    recepies = Receipt.objects.filter(~Q(ingredients=product))
    context = {'product': product, 'recipes': recepies}
    return render(request, 'cooking/alergic.html', context)

