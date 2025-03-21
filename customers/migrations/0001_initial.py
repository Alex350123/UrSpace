# Generated by Django 4.2.20 on 2025-03-13 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("Customerid", models.AutoField(primary_key=True, serialize=False)),
                ("firstname", models.CharField(max_length=100)),
                ("lastname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15)),
                ("DOB", models.DateField(blank=True)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CustomerToken",
            fields=[
                (
                    "key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to="customers.customer",
                    ),
                ),
            ],
        ),
    ]
