# Generated by Django 3.2.6 on 2022-03-25 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_order_pay_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pay_status',
        ),
    ]