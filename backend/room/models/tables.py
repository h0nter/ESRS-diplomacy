from django.db import models
from django.utils.translation import gettext_lazy as _

class Map(models.Model):
    name = models.CharField(max_length=30)
    max_countries = models.IntegerField()

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    can_float = models.BooleanField()
    class Meta:
        verbose_name_plural = 'Units'

class Country(models.Model):
    # will have user ID assoiated with it??
    name = models.CharField(max_length=30)
    map = models.ForeignKey(Map,on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=30)
    unit_spawn = models.BooleanField()
    is_sea = models.BooleanField()
    is_coast = models.BooleanField()
    map = models.ForeignKey(Map,on_delete=models.CASCADE)
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)

    # what is verbose name?
    class Meta:
        verbose_name_plural = 'Locations'
    def __str__(self):
        return self.name

# the location and what is next to itself
class Next_to(models.Model):
    # not sure on on delete here
    # only one type of location but many next_tos
    location = models.OneToOneField(Location,on_delete=models.CASCADE)
    next_to = models.ForeignKey(Location,on_delete=models.CASCADE)


class Order(models.Model):

    class MoveType(models.TextChoices):
        HOLD = 'HLD', _('Hold')
        MOVE = 'MVE' , _('Move')
        SUPPORT = 'SPT', _('Support')
        CONVOY = 'CVY', _('Convoy')

    order = models.CharField(max_length=3,choices=MoveType.choices,default=MoveType.HOLD)
    # want the order to be kept for history, even if unit is destoryed later?
    target_unit = models.ForeignKey(Unit,on_delete=models.DO_NOTHING) # Not null
    current_location = models.ForeignKey(Location,on_delete=models.DO_NOTHING) # Not null
    reference_unit = models.ForeignKey(Unit,on_delete=models.DO_NOTHING)
    reference_unit_current_location = models.ForeignKey(Location,on_delete=models.DO_NOTHING)
    reference_unit_new_location = models.ForeignKey(Location,on_delete=models.DO_NOTHING)


class Outcome(Order):
    # copy of Orders - show the orders that actually happened
    class Meta:
        proxy = True

