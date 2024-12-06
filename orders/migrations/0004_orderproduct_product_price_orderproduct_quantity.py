# Generated by Django 5.1.1 on 2024-10-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
