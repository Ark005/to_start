# Generated by Django 3.1.3 on 2021-02-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20210128_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsizes',
            name='b',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boxsizes',
            name='k',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
