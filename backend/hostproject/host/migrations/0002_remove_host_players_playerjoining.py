# Generated by Django 4.1.6 on 2023-05-04 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("host", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="host",
            name="players",
        ),
        migrations.CreateModel(
            name="PlayerJoining",
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
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="joined_player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="joined_room",
                        to="host.host",
                    ),
                ),
            ],
        ),
    ]