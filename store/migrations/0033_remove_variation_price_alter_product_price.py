# Generated by Django 5.1.1 on 2024-10-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_variation_price_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='price',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]