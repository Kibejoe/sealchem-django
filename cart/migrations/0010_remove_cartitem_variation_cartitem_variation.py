# Generated by Django 5.1.1 on 2024-10-25 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_remove_cartitem_variation_cartitem_variation'),
        ('store', '0037_alter_variation_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variation',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
