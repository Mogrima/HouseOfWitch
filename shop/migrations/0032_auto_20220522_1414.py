# Generated by Django 3.1.4 on 2022-05-22 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_cart_total_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='in_active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
    ]
