# Generated by Django 3.2.6 on 2022-03-20 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(auto_now=True, verbose_name='Дата создания заказа'),
        ),
    ]
