# Generated by Django 5.1.1 on 2024-10-24 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]