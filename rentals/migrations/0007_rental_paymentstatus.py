# Generated by Django 4.2.20 on 2025-03-19 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0006_remove_rental_paymentstatus_rental_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="rental",
            name="paymentstatus",
            field=models.BooleanField(default=False),
        ),
    ]
