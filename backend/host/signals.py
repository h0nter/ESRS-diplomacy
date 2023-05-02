# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models.player import Player

# @receiver(post_save, sender=User)
# def post_save_receiver(sender, instance, created, **kwargs):
#     # Your code logic here
#     if created:
#         Player.objects.create(user=instance, pk=instance.pk)
#     else:
#         print(instance, ' was not created!')
    
