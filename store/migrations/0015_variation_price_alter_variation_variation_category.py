# Generated by Django 5.1.1 on 2024-10-24 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('package', 'package')], max_length=100),
        ),
    ]
