from django.db import models
from django.utils.translation import gettext_lazy as _
from .order import Turn
import datetime


class Room(models.Model):
    
    class StatusType(models.TextChoices):
        Registered = 'Register', _('registered')
        Initializing = 'Init', _('Initial')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        retreating = 'Retreat', _('retreating ')
        Ending = 'End', _('Ending')
        Closed = 'Closed', _('Closed')

    room_name = models.CharField(max_length=30)
    room_status = models.CharField(max_length=8,choices=StatusType.choices,default=StatusType.Initializing)
    current_turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING, related_name='current_turn',blank=True,null=True)
    status = models.CharField(max_length=6, default='Open')
    close_time = models.DateTimeField(null=True)
    
    def initial_room(self):
        self.room_status = 'Init'
        self.save()
        self.current_turn = Turn.objects.create(year=1901)
        self.set_close_time()
        self.room_status = 'Wait'
        self.save()

     # set the close_time while save, automatactly add 2 hours
    def set_close_time(self):
        self.close_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.save()
