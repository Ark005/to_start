# Generated by Django 3.1.3 on 2021-01-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20210113_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='preview_text',
            field=models.TextField(blank=True, max_length=60, null=True, verbose_name='Preview Text'),
        ),
    ]