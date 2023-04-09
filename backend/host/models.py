from django.db import models
from django.utils.translation import gettext_lazy as _
from room.models.order import Turn
from django.contrib.auth.models import User

# status for each room
class Room(models.Model):
    class StatusType(models.TextChoices):
        Initial = 'Init', _('Initial')
        Opening = 'Open', _('Opening')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        Ending = 'End', _('Ending')
        Closed = 'Closed', _('Closed')

    room_status = models.CharField(max_length=5,choices=StatusType.choices,default=StatusType.Initial)
    turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING, related_name='room_turn', default=Turn.get)
    room_ID = models.IntegerField(unique=True, primary_key=True)
    hoster = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hoster')
    players = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = 'Room'

    def __str__(self):
        return str(self.pk)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    joining_rooms = models.ManyToManyField(Room)
    invitations = models.ManyToManyField(Room)
