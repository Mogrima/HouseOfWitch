# Generated by Django 3.2.6 on 2022-04-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_order_buying_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=1024, verbose_name='Комментарий к заказу'),
        ),
    ]
