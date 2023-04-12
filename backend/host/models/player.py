from django.db import models
from django.contrib.auth.models import User
import host.models.room as room


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_user')
    joining_rooms = models.ManyToManyField(room.Room,related_name='joining_rooms')
    invitations = models.ManyToManyField(room.Room, related_name='invitations')

    def __str__(self):
        return self.get_username()
    
