# Generated by Django 3.1.4 on 2022-05-15 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_auto_20220514_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='meta_description',
            field=models.CharField(blank=True, max_length=500, verbose_name='Meta-description'),
        ),
    ]
