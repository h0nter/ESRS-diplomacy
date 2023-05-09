from django.db import models
from room.models.map import Map


class Country(models.Model):

    name = models.CharField(max_length=10)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10)

    def __str__(self):
        return '' + self.name

    class Meta:
        verbose_name_plural = 'Countries'