# Generated by Django 3.2.6 on 2022-04-06 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='buying_type',
        ),
    ]
