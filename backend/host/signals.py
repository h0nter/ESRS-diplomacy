from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def post_save_receiver(sender, instance, created, **kwargs):
    # Your code logic here
    print('Signal received: User object saved')
