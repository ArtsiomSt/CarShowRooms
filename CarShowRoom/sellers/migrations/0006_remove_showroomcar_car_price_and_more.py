# Generated by Django 4.2 on 2023-04-26 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sellers", "0005_alter_showroomcar_dealer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="showroomcar",
            name="car_price",
        ),
        migrations.RemoveField(
            model_name="showroomcar",
            name="currency",
        ),
    ]
