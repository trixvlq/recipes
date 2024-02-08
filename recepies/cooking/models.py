from django.contrib.auth.models import User
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
    usage = models.PositiveIntegerField(default=0, verbose_name='Количество использований')
    ingredients = models.ManyToManyField('Ingredient', verbose_name='Ингредиенты', through='RecipeIngredient')
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/', verbose_name='Картинка рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        indexes = [
            models.Index(fields=["title"])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})


class RecipeStep(models.Model):
    number = models.PositiveIntegerField(default=1, verbose_name='Номер шага')
    title = models.CharField(max_length=255, verbose_name='Название шага')
    description = models.TextField(verbose_name='Описание шага', null=True)
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name='Рецепт', related_name='recipe_steps')

    class Meta:
        verbose_name = 'Шаг готовки'
        verbose_name_plural = 'Шаги готовки'

    def __str__(self):
        return f'{self.number} step to {self.recipe.title}'


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
    title = models.CharField(max_length=255, verbose_name='Имя ингредиента', unique=True)
    description = models.TextField(verbose_name='Описание продукта')
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/', verbose_name='Картинка ингредиента')
    carbs = models.FloatField(default=1, verbose_name='Углеводы')
    fats = models.FloatField(default=1, verbose_name='Жиры')
    protein = models.FloatField(default=1, verbose_name='Белки')
    vegan = models.BooleanField(verbose_name='Вегетарианская')
    halal = models.BooleanField(verbose_name='Халяль')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class RequestIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField(max_length=255, verbose_name='Имя ингредиента')
    description = models.TextField(verbose_name='Описание продукта')
    image = models.ImageField(upload_to='static/images/%Y/%m/%d/', verbose_name='Картинка ингредиента')
    carbs = models.FloatField(default=1, verbose_name='Углеводы')
    fats = models.FloatField(default=1, verbose_name='Жиры')
    protein = models.FloatField(default=1, verbose_name='Белки')
    calories = models.FloatField(default=1, verbose_name='Калорийность')
    vegan = models.BooleanField(verbose_name='Вегетарианская')
    halal = models.BooleanField(verbose_name='Халяль')
    is_active = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заявка в ингредиенты'
        verbose_name_plural = 'Заявки в ингредиенты'

    def __str__(self):
        return f'{self.user.username} suggests {self.title}'
