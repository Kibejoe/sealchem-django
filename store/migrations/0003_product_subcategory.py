# Generated by Django 5.1.1 on 2024-10-06 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_subcategory'),
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.subcategory'),
        ),
    ]
