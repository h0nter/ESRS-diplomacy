from django.db.models.signals import post_save
from django.dispatch import receiver
from host.models.host import Host
from room.models.broadcast import Room

@receiver(post_save, sender=Room)
def post_save_receiver(sender, instance, created, **kwargs):
    if not created:
        # Room object updated
        pass
    else:
        # Room be created
        pass