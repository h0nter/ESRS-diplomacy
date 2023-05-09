# Generated by Django 4.1.6 on 2023-05-08 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("host", "0010_host_room_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="host",
            name="room_status",
            field=models.CharField(
                choices=[
                    ("REGISTERD", "registered"),
                    ("INITIALIZE", "initialize"),
                    ("WAIT", "Orders Incoming, Players Debating"),
                    ("RESOLVE", "Resolving Orders"),
                    ("RETREAT", "Orders Incoming, Only Players Retreating"),
                    ("UPDATE", "Update map with new Unit Positions"),
                    ("RESUPP", "Gaining Units After FALL"),
                    ("CHECK", "Check the closing conditions"),
                    ("CLOSED", "Will only change the status when room is closed"),
                ],
                default="REGISTERD",
                max_length=10,
            ),
        ),
    ]