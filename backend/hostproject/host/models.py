import secrets
import string
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# status for each room
class Host(models.Model):
    class StatusType(models.TextChoices):
        Registered = 'Register', _('registered')
        Initializing = 'Init', _('Initial')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        retreating = 'Retreat', _('retreating ')
        Ending = 'End', _('Ending')
        Closed = 'Closed', _('Closed')

    hoster = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hoster')
    room_name = models.CharField(max_length=30)
    room_code = models.CharField(max_length=6, default='')
    room_status = models.CharField(max_length=8,choices=StatusType.choices,default=StatusType.Registered)
    max_players = models.PositiveSmallIntegerField(default=7)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.PositiveSmallIntegerField(default=8080)

    class Meta:
        verbose_name_plural = 'Room'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.room_code = ''.join(secrets.choice(string.ascii_letters).capitalize() for _ in range(5))
        super(Host, self).save(*args, **kwargs)


class UserRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='joined_player')
    room = models.ForeignKey(Host, on_delete=models.DO_NOTHING, related_name='joined_room')

    def __str__(self):
        return self.player.get_username()