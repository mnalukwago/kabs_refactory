# Generated by Django 5.2 on 2025-05-04 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kglapp', '0004_delete_product_delete_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditsale',
            name='amount_paid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
