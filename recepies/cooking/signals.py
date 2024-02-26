from django.db import transaction

from cooking.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


@receiver(post_save, sender=Recipe)
def change_status(sender, instance, **kwargs):
    instance.check_vegan()
    instance.check_halal()
    Recipe.objects.filter(pk=instance.pk).update(vegan=instance.vegan, halal=instance.halal)


@receiver(post_save, sender=Ingredient)
def check_recipies_status(sender, created, instance, **kwargs):
    recepies = instance.ingredient_in_recipe.all()
    for recipe in recepies:
        recipe.check_vegan()
        recipe.check_halal()
        recipe.save(update_fields=['vegan', 'halal'])