# Generated by Django 5.1.1 on 2024-10-22 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_sub_category'),
        ('store', '0011_remove_product_subcategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sub_Category',
        ),
    ]