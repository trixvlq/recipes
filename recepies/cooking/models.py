from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class Dish(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название блюда')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название рецепта')
    slug = AutoSlugField(unique=True, populate_from='title', verbose_name='Слаг')
    dish_type = models.ForeignKey('Dish', on_delete=models.CASCADE, verbose_name='Вид блюда')
    description = models.TextField(verbose_name='Описание')
    process = models.TextField(verbose_name='Инструкция')
    usage = models.PositiveIntegerField(default=0, verbose_name='Количество использований')
    ingredients = models.ManyToManyField('Ingredient', verbose_name='Ингредиенты', through='RecipeIngredient')
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/', verbose_name='Картинка рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})


class RecipeStep(models.Model):
    number = models.PositiveIntegerField(default=1, verbose_name='Номер шага')
    title = models.CharField(max_length=255, verbose_name='Название шага')
    description = models.TextField(verbose_name='Описание шага', null=True)
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Шаг готовки'
        verbose_name_plural = 'Шаги готовки'

    def __str__(self):
        return f'{self.number} step to {self.recipe}'


class RecipeIngredient(models.Model):
    UNITS = (
        ("мл", "Миллилитры"),
        ("г", "Граммы"),
        ("ст.л.", "Столовые ложки"),
        ("шт", "Штуки"),
    )
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name='Рецепт',
                               related_name='detailed_ingredients')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, verbose_name='Ингредиент')
    units = models.CharField(max_length=255, choices=UNITS, verbose_name='Единицы измерения')
    amount = models.IntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.ingredient.title} to {self.recipe.title}'


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя ингредиента')
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/', verbose_name='Картинка ингредиента')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title
