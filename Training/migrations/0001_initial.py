# Generated by Django 3.2.9 on 2022-02-16 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest', models.BooleanField(default=True)),
                ('roll', models.BooleanField(default=True)),
                ('salute', models.BooleanField(default=True)),
                ('Resttodown', models.BooleanField(default=True)),
                ('hifi', models.BooleanField(default=True)),
                ('longstay', models.BooleanField(default=True)),
                ('fetch', models.BooleanField(default=True)),
                ('crawl', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'AdvancedTraining',
            },
        ),
        migrations.CreateModel(
            name='BasicTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heelwalk', models.BooleanField(default=True)),
                ('down', models.BooleanField(default=True)),
                ('stop', models.BooleanField(default=True)),
                ('downtosit', models.BooleanField(default=True)),
                ('sit', models.BooleanField(default=True)),
                ('shakehand', models.BooleanField(default=True)),
                ('standstay', models.BooleanField(default=True)),
                ('distancecontrol', models.BooleanField(default=True)),
                ('come', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'BasicTraining',
            },
        ),
        migrations.CreateModel(
            name='Enquireform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personname', models.CharField(default='', max_length=60, null=True)),
                ('phone_no', models.CharField(default='', max_length=13, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('Address', models.CharField(default='', max_length=200, null=True)),
                ('country', models.CharField(default='', max_length=50, null=True)),
                ('state', models.CharField(default='', max_length=60, null=True)),
                ('city', models.CharField(default='', max_length=100, null=True)),
                ('zipcode', models.IntegerField()),
                ('petname', models.CharField(choices=[('D', 'Dog'), ('C', 'Cat'), ('O', 'Other')], default='', max_length=10)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=9)),
                ('upload', models.FileField(upload_to='')),
                ('trainingkit', models.CharField(choices=[('BasicTraining', 'BasicTraining'), ('AdvancedTraining', ' AdvancedTraining')], default='', max_length=50)),
            ],
        ),
    ]
