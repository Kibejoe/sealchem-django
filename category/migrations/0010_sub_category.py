# Generated by Django 5.1.1 on 2024-10-22 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0009_remove_category_level_remove_category_lft_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
    ]
