# Generated by Django 5.1.1 on 2024-10-24 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('package', 'package'), ('price', 'price')], max_length=100),
        ),
    ]