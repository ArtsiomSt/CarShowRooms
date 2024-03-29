# Generated by Django 4.2 on 2023-04-20 09:04

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models

import core.validation.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CarBrand",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=30, unique=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("slug", models.SlugField(max_length=30, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Car",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=40)),
                (
                    "doors_amount",
                    models.IntegerField(
                        default=3,
                        validators=[core.validation.validators.validate_positive],
                    ),
                ),
                (
                    "engine_power",
                    models.IntegerField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                (
                    "engine_type",
                    models.CharField(
                        choices=[
                            ("FUEL", "Fuel"),
                            ("DIESEL", "Diesel"),
                            ("HYBRID", "Hybrid"),
                            ("GAS", "Gas"),
                            ("ELECTRICITY", "Electricity"),
                        ],
                        default="FUEL",
                        max_length=20,
                    ),
                ),
                (
                    "year_produced",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1900,
                                message="Year should be greater than 1900",
                            )
                        ]
                    ),
                ),
                (
                    "price_category",
                    models.CharField(
                        choices=[
                            ("CHEAP", "Cheap"),
                            ("MEDIUM", "Medium"),
                            ("LUXURY", "Luxury"),
                        ],
                        default="MEDIUM",
                        max_length=20,
                    ),
                ),
                (
                    "length",
                    models.FloatField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                (
                    "width",
                    models.FloatField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                (
                    "height",
                    models.FloatField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                (
                    "max_speed",
                    models.IntegerField(
                        validators=[core.validation.validators.validate_positive]
                    ),
                ),
                (
                    "car_brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cars",
                        to="cars.carbrand",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
