# Generated by Django 4.2.4 on 2023-08-29 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("community_boards", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="likes_user",
            field=models.ManyToManyField(
                blank=True,
                related_name="boards_liked",
                to=settings.AUTH_USER_MODEL,
                verbose_name="좋아요 목록",
            ),
        ),
        migrations.AddField(
            model_name="board",
            name="writer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="boards_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]