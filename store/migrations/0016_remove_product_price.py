# Generated by Django 5.1.1 on 2024-10-24 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_variation_price_alter_variation_variation_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
