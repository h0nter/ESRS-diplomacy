from django.db import models
from host.models import User
from .tables import Country


class player(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE)
    Country = models.ForeignKey(Country,on_delete=models.DO_NOTHING)
    # conditions for closing the game
    territory = models.IntegerField()
    alive = models.BooleanField(default=True)
