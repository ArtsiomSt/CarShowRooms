# Generated by Django 4.2 on 2023-04-26 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sellers", "0003_discount_discount_percent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discount",
            name="car_showroom",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discounts",
                to="sellers.carshowroom",
            ),
        ),
        migrations.AlterField(
            model_name="discount",
            name="dealer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discounts",
                to="sellers.dealer",
            ),
        ),
    ]