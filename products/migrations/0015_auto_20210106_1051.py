# Generated by Django 3.1.3 on 2021-01-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20210106_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='t',
            field=models.IntegerField(),
        ),
    ]