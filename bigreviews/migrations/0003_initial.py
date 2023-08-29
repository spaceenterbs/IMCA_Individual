# Generated by Django 4.2.4 on 2023-08-29 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bigreviews", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bigreview",
            name="bigreview_writer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bigreviews_writer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]