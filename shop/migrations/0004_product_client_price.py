# Generated by Django 2.0 on 2020-12-23 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20201220_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='client_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]