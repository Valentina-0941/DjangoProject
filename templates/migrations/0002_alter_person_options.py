# Generated by Django 5.0.1 on 2024-01-09 12:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("templates", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name": "Человек", "verbose_name_plural": "Люди"},
        ),
    ]
