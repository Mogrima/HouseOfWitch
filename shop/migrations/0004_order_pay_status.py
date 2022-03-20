# Generated by Django 3.2.6 on 2022-03-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_goods_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_status',
            field=models.CharField(choices=[('unpaid ', 'Неоплачен'), ('pay_inprogress', 'Платеж в обработке'), ('paid', 'Оплачен')], default='unpaid ', max_length=100, verbose_name='Статус платежа'),
        ),
    ]
