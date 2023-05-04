from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=Room)
# def post_save_receiver(sender, instance, created, **kwargs):
#     if not created:
#         # Room object updated
#         pass
#     else:
#         # Room be created
#         pass