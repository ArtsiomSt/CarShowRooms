# Generated by Django 4.2 on 2023-04-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0002_alter_car_created_at_alter_car_modified_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carbrand",
            name="slug",
            field=models.SlugField(default="migration", max_length=30, unique=True),
            preserve_default=False,
        ),
    ]