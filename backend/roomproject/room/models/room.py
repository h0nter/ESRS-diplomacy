import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from .turn import Turn
from .map import Map


class RoomStatus(models.TextChoices):

    REGISTERED =  'REGISTERD', _('registered')

    # Loops
    WAITING = 'WAIT', _('Orders Incoming, Players Debating')
    RESOLVE = 'RESOLVE', _('Resolving Orders')
    RETREAT = 'RETREAT', _('Orders Incoming, Only Players Retreating') # Goes back to Resolve, this time just MVEs, and Players can only MVE to certain places
    UPDATE = 'UPDATE', _('Update map with new Unit Positions') 
    RESUPPLY = 'RESUPP', _('Gaining Units After FALL')
    CHECKING = 'CHECK', _('Check the closing conditions')

    CLOSED = 'CLOSED', _('Will only change the status when room is closed')

class Room(models.Model):
    room_name = models.CharField(max_length=30)
    current_turn = models.ForeignKey(Turn, null=True, on_delete=models.DO_NOTHING, related_name='current_turn')
    status = models.CharField(max_length=9, choices=RoomStatus.choices,default=RoomStatus.REGISTERED)
    close_time = models.DateTimeField(null=True)
    map = models.ForeignKey(Map,on_delete=models.DO_NOTHING, related_name='room_map', default=1)

     # set the close_time while save, automatactly add 2 hours
    def set_close_time(self):
        self.close_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.save()

