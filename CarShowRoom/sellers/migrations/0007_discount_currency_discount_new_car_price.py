# Generated by Django 4.2 on 2023-04-27 08:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sellers", "0006_remove_showroomcar_car_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="discount",
            name="currency",
            field=models.CharField(
                choices=[
                    ("USD", "USD"),
                    ("EUR", "EUR"),
                    ("BYN", "BYN"),
                    ("RUB", "RUB"),
                ],
                default="USD",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="discount",
            name="new_car_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=7, null=True
            ),
        ),
    ]