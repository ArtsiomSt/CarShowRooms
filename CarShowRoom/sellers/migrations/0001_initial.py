# Generated by Django 4.2 on 2023-04-20 09:04

import core.validation.validators
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cars", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Balance",
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
                    "money_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
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
                    "last_deposit",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "last_spent",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CarShowRoom",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=40, unique=True)),
                ("city", models.CharField(max_length=40)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("address", models.TextField()),
                (
                    "margin",
                    models.FloatField(
                        validators=[core.validation.validators.validate_positive]
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
                        max_length=10,
                    ),
                ),
                (
                    "balance",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="car_showroom",
                        to="sellers.balance",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Dealer",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=40, unique=True)),
                (
                    "year_founded",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1800,
                                message="Year should be greater than 1800",
                            )
                        ]
                    ),
                ),
                (
                    "balance",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dealer",
                        to="sellers.balance",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ShowroomCar",
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
                ("car_amount", models.IntegerField(default=1)),
                ("car_sold", models.IntegerField(default=0)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
                (
                    "car_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sellers.carshowroom",
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sellers.dealer"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowroomBrand",
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
                    "car_brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.carbrand"
                    ),
                ),
                (
                    "car_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sellers.carshowroom",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DealerShowroom",
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
                ("deals_amount", models.IntegerField(default=1)),
                ("discount", models.FloatField(default=0)),
                (
                    "car_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sellers.carshowroom",
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sellers.dealer"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DealerCar",
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
                ("car_sold", models.IntegerField(default=0)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sellers.dealer"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="dealer",
            name="car_list",
            field=models.ManyToManyField(
                related_name="dealers", through="sellers.DealerCar", to="cars.car"
            ),
        ),
        migrations.AddField(
            model_name="carshowroom",
            name="car_brands",
            field=models.ManyToManyField(
                related_name="car_showrooms",
                through="sellers.ShowroomBrand",
                to="cars.carbrand",
            ),
        ),
        migrations.AddField(
            model_name="carshowroom",
            name="car_list",
            field=models.ManyToManyField(
                related_name="car_showrooms",
                through="sellers.ShowroomCar",
                to="cars.car",
            ),
        ),
    ]
