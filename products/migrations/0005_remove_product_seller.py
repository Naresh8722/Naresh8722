# Generated by Django 3.2.9 on 2022-03-28 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_qunitity_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
    ]