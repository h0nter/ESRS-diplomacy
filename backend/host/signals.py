from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.player import Player


# A post_save signal received when a User instance is created
@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
