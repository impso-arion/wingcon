# Generated by Django 3.0.2 on 2021-08-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
