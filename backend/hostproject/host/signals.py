from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Host
from .models import UserHost, RoomStatus


@receiver(post_save, sender=Host)
def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        # Room be created
        UserHost.objects.create(user=instance.hoster, room=instance).save()
    else:
        if instance.status == RoomStatus.CLOSED:
            print(instance.room_name,' room closed')