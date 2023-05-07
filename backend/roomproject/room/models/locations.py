from django.db import models
from django.utils.translation import gettext_lazy as _


class Map(models.Model):
    name = models.CharField(max_length=30)
    max_countries = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Maps'
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=15)
    map = models.ForeignKey(Map,on_delete=models.CASCADE)
    colour = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Countries'

class Location(models.Model):
    name = models.CharField(max_length=30)
    unit_spawn = models.BooleanField(default=False)
    is_sea = models.BooleanField(default=False)
    is_coast = models.BooleanField(default=False)
    map = models.ForeignKey(Map,on_delete=models.CASCADE)
    text_pos_x = models.CharField(max_length=10)
    text_pos_y = models.CharField(max_length=10) 
    current_owner = models.ForeignKey(Country,blank=True,null=True,on_delete=models.DO_NOTHING)
    abbreviation = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'Locations'
    def __str__(self):
        return self.name

# a location can have many polygons
class Map_Polygon(models.Model):
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    polygon = models.CharField(max_length=500)
    colour = models.CharField(max_length=10)
    class Meta:
        verbose_name_plural = 'Map_Polygons'
    def __str__(self):
        return self.pk

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
