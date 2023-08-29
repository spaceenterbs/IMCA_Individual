# Generated by Django 4.2.4 on 2023-08-29 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Calendar",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("poster", models.URLField(blank=True, null=True)),
                ("place", models.CharField(max_length=15)),
                ("runtime", models.TimeField(blank=True, null=True)),
                ("price", models.PositiveIntegerField(blank=True, null=True)),
                ("name", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name_plural": "calendars",
            },
        ),
        migrations.CreateModel(
            name="Memo",
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
                ("content", models.TextField()),
                (
                    "calendar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memos",
                        to="calenders.calendar",
                    ),
                ),
            ],
        ),
    ]
