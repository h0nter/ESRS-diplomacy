from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Host
from .models import PlayerJoining


@receiver(post_save, sender=Host)
def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        # Room be created
        PlayerJoining.objects.create(player=instance.hoster, room=instance).save()
    else:
        if instance.room_status == 'Closed':
            print(instance.room_name,' room closed')