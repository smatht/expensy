# Generated by Django 4.2 on 2025-07-16 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        db_column="id", primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("alt_name", models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                "db_table": "categories",
            },
        ),
        migrations.CreateModel(
            name="Records",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="id", max_length=40, primary_key=True, serialize=False
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=350, null=True),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("time", models.TimeField(blank=True, null=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("sync", models.BooleanField(default=False)),
                ("source", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data.categories",
                    ),
                ),
            ],
            options={
                "db_table": "records",
            },
        ),
    ]
