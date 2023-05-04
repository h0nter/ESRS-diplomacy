from django.db import models
from django.contrib.auth.models import User
from .locations import Country
from .order import Turn, Unit
import datetime
from django.utils.translation import gettext_lazy as _


class Player(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='player_user')
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING,null=True, related_name='player_country')
    # conditions for closing the game
    is_alive = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=True)

class RoomStatus(models.TextChoices):

    INITIAL = 'INIT', _('Formating the room database')
    OPEN =  'OPEN', _('Waiting for user to login the game')

    # Loops
    WAITING = 'WAIT', _('Orders Incoming, Players Debating')
    RESOLVE = 'RESOLVE', _('Resolving Orders')
    RETREAT = 'RETREAT', _('Orders Incoming, Only Players Retreating')
    # Goes back to Resolve, this time just MVEs
    # Players can only MVE to certain places
    UPDATE = 'UPDATE', _('Update map with new Unit Positions')
    RESUPPLY = 'RESUPP', _('Gaining Units After FALL')
    CHECKING = 'CHECK', _('Check the closing conditions')

    CLOSED = 'CLOSED', _('Will only change the status when room is closed')

class Room(models.Model):
    room_name = models.CharField(max_length=30)
    current_turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING, related_name='current_turn')
    status = models.CharField(max_length=7, choices=RoomStatus.choices,default=RoomStatus.INITIAL)
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

class PlayerRoom(models.Model):
    # relate the player and the room together
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name_plural = 'PlayersRooms'