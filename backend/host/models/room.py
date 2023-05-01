from django.db import models
from django.utils.translation import gettext_lazy as _
from room.models.order import Turn
from django.contrib.auth.models import User
import secrets
import string

# status for each room
class Room(models.Model):
    class StatusType(models.TextChoices):
        Initial = 'Init', _('Initial')
        Opening = 'Open', _('Opening')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        Ending = 'End', _('Ending')
        Closed = 'Closed', _('Closed')

    room_name = models.CharField(max_length=30, primary_key=True)
    id = models.IntegerField(null=True)
    code = models.CharField(max_length=6, default='')
    room_status = models.CharField(max_length=6,choices=StatusType.choices,default=StatusType.Initial)
    current_turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING, related_name='current_turn',blank=True,null=True)
    hoster = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hoster')
    players = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = 'Room'

    def __str__(self):
        return str(self.pk)

    def initial_room(self):
        self.id = hash(self.room_name)[:8]
        self.players.add(self.hoster)
        self.current_turn = Turn.objects.create(year=1901)
        self.code = ''.join(secrets.choice(string.ascii_letters).capitalize() for _ in range(5))
        self.save()







