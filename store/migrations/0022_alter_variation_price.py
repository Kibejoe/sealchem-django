# Generated by Django 5.1.1 on 2024-10-24 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_variation_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
