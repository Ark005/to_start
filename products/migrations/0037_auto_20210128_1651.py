# Generated by Django 3.0.6 on 2021-01-28 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_auto_20210128_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxsizes',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
