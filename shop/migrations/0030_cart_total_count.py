# Generated by Django 3.1.4 on 2022-05-18 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_article_meta_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Все кол-во товаров'),
        ),
    ]