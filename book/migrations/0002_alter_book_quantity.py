# Generated by Django 4.1.3 on 2022-11-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]