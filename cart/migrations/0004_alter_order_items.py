# Generated by Django 3.2.9 on 2022-03-14 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20220226_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='cart.Cart'),
        ),
    ]