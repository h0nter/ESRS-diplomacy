from django.db import models
from django.contrib.auth.models import User
from .locations import Country
from .order import Turn
import datetime


class Player(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING,null=True)
    # conditions for closing the game
    territory = models.IntegerField(default=3)
    alive = models.BooleanField(default=True)


class Room(models.Model):
    room_name = models.CharField(max_length=30)
    current_turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING, related_name='current_turn',blank=True,null=True)
    status = models.CharField(max_length=6)
    build_time = models.DateTimeField(auto_now_add=True)
    close_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def initial_room(self):
        self.room_status = 'Init'
        self.save()
        self.current_turn = Turn.objects.create(year=1901)
        self.set_close_time()
        self.room_status = 'Wait'
        self.save()

     # set the close_time while save, automatactly add 2 hours
    def set_close_time(self):
        self.build_time = datetime.datetime.now()
        self.close_time = self.build_time + datetime.timedelta(hours=2)
        self.save()