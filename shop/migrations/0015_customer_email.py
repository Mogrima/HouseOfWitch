# Generated by Django 3.2.6 on 2022-03-29 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Email'),
        ),
    ]
