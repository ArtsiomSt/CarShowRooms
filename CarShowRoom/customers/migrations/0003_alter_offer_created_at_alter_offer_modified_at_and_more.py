# Generated by Django 4.2 on 2023-04-14 19:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]