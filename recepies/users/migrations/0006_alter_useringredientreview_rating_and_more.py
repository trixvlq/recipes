# Generated by Django 5.0.1 on 2024-02-20 13:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_subcomments_useringredientreview_subcomment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useringredientreview',
            name='rating',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='userrecipereview',
            name='rating',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка'),
        ),
    ]
