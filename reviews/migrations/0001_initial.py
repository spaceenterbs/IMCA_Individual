# Generated by Django 4.2.4 on 2023-08-29 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("community_boards", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("review_content", models.CharField(max_length=140)),
                ("is_blocked", models.BooleanField(default=False)),
                (
                    "review_board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="community_boards.board",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
