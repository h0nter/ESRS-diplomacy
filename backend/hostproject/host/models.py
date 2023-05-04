import secrets
import string
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# status for each room
class Host(models.Model):
    class StatusType(models.TextChoices):
        Opening = 'Open', _('Opening')
        Initial = 'Init', _('Initial')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        Ending = 'End', _('Ending')
        Closed = 'Closed', _('Closed')

    room_name = models.CharField(max_length=30)
    room_code = models.CharField(max_length=6, default='')
    room_status = models.CharField(max_length=6,choices=StatusType.choices,default=StatusType.Opening)
    hoster = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hoster')
    players = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = 'Room'

    def __str__(self):
        return str(self.pk)

    
    def create(self):
        self.save()
        self.players.add(self.hoster.pk)
        self.room_code = ''.join(secrets.choice(string.ascii_letters).capitalize() for _ in range(5))
        self.save()


# class UserHost(models.Model):
#     user = models.ForeignKey(User)
#     room = models.ForeignKey(Room)