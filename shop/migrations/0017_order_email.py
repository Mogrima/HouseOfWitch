# Generated by Django 3.2.6 on 2022-04-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_order_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Электронная почта'),
        ),
    ]
