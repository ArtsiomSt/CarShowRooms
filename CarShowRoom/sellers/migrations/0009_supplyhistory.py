# Generated by Django 4.2 on 2023-04-28 11:48

import django.db.models.deletion
from django.db import migrations, models

import core.validation.validators


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0001_initial"),
        ("sellers", "0008_remove_discount_currency_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SupplyHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "car_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[core.validation.validators.validate_positive],
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("USD", "USD"),
                            ("EUR", "EUR"),
                            ("BYN", "BYN"),
                            ("RUB", "RUB"),
                        ],
                        default="USD",
                        max_length=40,
                    ),
                ),
                (
                    "cars_amount",
                    models.IntegerField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                ("date_of_supply", models.DateTimeField(auto_now_add=True)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="supplies",
                        to="cars.car",
                    ),
                ),
                (
                    "car_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="supplies",
                        to="sellers.carshowroom",
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="supplies",
                        to="sellers.dealer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
