# Generated by Django 4.1.6 on 2023-05-05 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("host", "0006_userroom_delete_playerroom"),
    ]

    operations = [
        migrations.AlterField(
            model_name="host",
            name="room_status",
            field=models.CharField(
                choices=[
                    ("Register", "registered"),
                    ("Init", "Initial"),
                    ("Wait", "Waiting"),
                    ("Check", "Checking"),
                    ("Retreat", "retreating "),
                    ("End", "Ending"),
                    ("Closed", "Closed"),
                ],
                default="Register",
                max_length=8,
            ),
        ),
    ]
