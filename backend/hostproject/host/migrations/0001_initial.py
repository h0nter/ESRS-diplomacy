# Generated by Django 4.1.6 on 2023-05-03 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Host",
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
                ("room_name", models.CharField(max_length=30)),
                ("room_code", models.CharField(default="", max_length=6)),
                (
                    "room_status",
                    models.CharField(
                        choices=[
                            ("Open", "Opening"),
                            ("Init", "Initial"),
                            ("Wait", "Waiting"),
                            ("Check", "Checking"),
                            ("End", "Ending"),
                            ("Closed", "Closed"),
                        ],
                        default="Open",
                        max_length=6,
                    ),
                ),
                (
                    "hoster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="hoster",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("players", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name_plural": "Room",
            },
        ),
    ]
