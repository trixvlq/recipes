from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cooking.models import *


class IngredientRecords(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='IngredientRecord',
                                   verbose_name='Ингредиент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserRecord',
                             verbose_name='Пользователь')
    amount = models.IntegerField(validators=[
        MinValueValidator(0)
    ], verbose_name='Количество использований', default=0)

    class Meta:
        verbose_name = 'Рекорд пользователя'
        verbose_name_plural = 'Рекорды пользователей'


class UserReview(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    content = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка', null=True)

    class Meta:
        abstract = True


class UserIngredientReview(UserReview):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент',
                                   related_name='reviews')

    class Meta:
        verbose_name = 'Комментарий на ингредиент'
        verbose_name_plural = 'Комментарии на игредиенты'


class UserRecipeReview(UserReview):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='reviews')


    class Meta:
        verbose_name = 'Комментарий на рецепт'
        verbose_name_plural = 'Комментарии на рецепты'
