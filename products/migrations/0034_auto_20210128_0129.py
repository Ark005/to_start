# Generated by Django 3.0.6 on 2021-01-27 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='box_size',
            field=models.CharField(default='80х80х40', max_length=50),
        ),
    ]
