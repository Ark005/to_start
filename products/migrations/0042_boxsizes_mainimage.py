# Generated by Django 3.1.3 on 2021-02-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_auto_20210202_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsizes',
            name='mainimage',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
