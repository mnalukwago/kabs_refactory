# Generated by Django 5.2 on 2025-05-04 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kglapp', '0005_creditsale_amount_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditsale',
            name='amount_paid',
        ),
    ]
