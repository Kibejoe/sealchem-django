# Generated by Django 4.2.16 on 2024-11-22 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_payment_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]