# Generated by Django 3.2.6 on 2022-03-20 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_order_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа'),
        ),
    ]
