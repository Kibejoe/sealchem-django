# Generated by Django 4.2.16 on 2024-11-29 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_checkout_request_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='checkout_request_id',
        ),
    ]
