# Generated by Django 4.2 on 2023-04-20 09:04

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.validation.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cars", "0001_initial"),
        ("core", "0001_initial"),
        ("sellers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                (
                    "balance",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="balance_customer",
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
            name="TransactionHistory",
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
                (
                    "deal_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=7,
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
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="cars.car",
                    ),
                ),
                (
                    "made_by_customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="customers.customer",
                    ),
                ),
                (
                    "sold_by_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transactions",
                        to="sellers.carshowroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowroomCustomer",
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
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
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
                (
                    "max_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=7,
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
                        max_length=20,
                    ),
                ),
                ("is_processed", models.BooleanField(default=False)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offers",
                        to="cars.car",
                    ),
                ),
                (
                    "made_by_customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offers",
                        to="customers.customer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="customer",
            name="showrooms",
            field=models.ManyToManyField(
                related_name="customers",
                through="customers.ShowroomCustomer",
                to="sellers.carshowroom",
            ),
        ),
    ]
