# Generated by Django 4.1.6 on 2023-05-07 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("host", "0009_alter_host_room_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="room_id",
            field=models.PositiveIntegerField(null=True),
        ),
    ]