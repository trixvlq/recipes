# Generated by Django 5.0.1 on 2024-02-20 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0004_recipe_halal_recipe_vegan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredient_in_recipe', through='cooking.RecipeIngredient', to='cooking.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_on_recipe', to='cooking.ingredient', verbose_name='Ингредиент'),
        ),
    ]
