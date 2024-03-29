from django.db import models
from django.utils.translation import gettext_lazy as _
from room.models.map import Map


class Location(models.Model):
    name = models.CharField(max_length=30)
    unit_spawn = models.BooleanField(default=False)
    is_sea = models.BooleanField(default=False)
    is_coast = models.BooleanField(default=False)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    text_pos_x = models.IntegerField(default=0)
    text_pos_y = models.IntegerField(default=0)

    abbreviation = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '' + self.name

# a location can have many polygons


class Map_Polygon(models.Model):
    class Polygon_Colour(models.TextChoices):
        LAND = 'LAND', _('LAND')
        AQUA = 'AQUA', _('AQUA')
        HASH = 'HASH', _('HASH')

    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='polygons')
    polygon = models.CharField(max_length=500)
    colour = models.CharField(max_length=4,choices=Polygon_Colour.choices,default=Polygon_Colour.LAND)

    class Meta:
        verbose_name_plural = 'Map_Polygons'

    def __str__(self):
        return '' + self.pk

# the location and what is next to itself


class Next_to(models.Model):
    # not sure on on delete here
    # only one type of location but many next_tos
    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='Next_to_location')
    next_to = models.ForeignKey(Location,on_delete=models.DO_NOTHING,related_name='next_to')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Next_to'
