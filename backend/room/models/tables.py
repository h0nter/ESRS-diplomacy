from django.db import models
from django.utils.translation import gettext_lazy as _

class Map(models.Model):
    name = models.CharField(max_length=30)
    max_countries = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Maps'

class Country(models.Model):
    # will have user ID assoiated with it??
    name = models.CharField(max_length=30)
    map = models.ForeignKey(Map,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Countries'

class Location(models.Model):
    name = models.CharField(max_length=30)
    unit_spawn = models.BooleanField()
    is_sea = models.BooleanField()
    is_coast = models.BooleanField()
    map = models.ForeignKey(Map,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Locations'
    def __str__(self):
        return self.name

# the location and what is next to itself
class Next_to(models.Model):
    # not sure on on delete here
    # only one type of location but many next_tos
    location = models.OneToOneField(Location,on_delete=models.CASCADE,related_name='location')
    next_to = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='next_to')

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    can_float = models.BooleanField()
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Units'

class Order(models.Model):

    class MoveType(models.TextChoices):
        HOLD = 'HLD', _('Hold')
        MOVE = 'MVE' , _('Move')
        SUPPORT = 'SPT', _('Support')
        CONVOY = 'CVY', _('Convoy')
    class Meta:
        verbose_name_plural = 'Orders'

    order = models.CharField(max_length=3,choices=MoveType.choices,default=MoveType.HOLD)
    # want the order to be kept for history, even if unit is destoryed later?
    target_unit = models.ForeignKey(Unit,on_delete=models.DO_NOTHING,related_name='target_unit') # Not null
    current_location = models.ForeignKey(Location,on_delete=models.DO_NOTHING,related_name='current_location') # Not null
    reference_unit = models.ForeignKey(Unit,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit')
    reference_unit_current_location = models.ForeignKey(Location,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_current_location')
    reference_unit_new_location = models.ForeignKey(Location,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_new_location')


class Outcome(Order):
    # copy of Orders - show the orders that actually happened
    class Meta:
        proxy = True
        verbose_name_plural = 'Outcomes'

