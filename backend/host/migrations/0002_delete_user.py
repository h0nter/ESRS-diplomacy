# Generated by Django 4.1.6 on 2023-03-21 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]