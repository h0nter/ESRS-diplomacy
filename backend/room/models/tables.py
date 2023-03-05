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
    # will have user ID assoiated with it??
    name = models.CharField(max_length=30)
    # map = models.ForeignKey(Map,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Countries'

class Location(models.Model):
    name = models.CharField(max_length=30)
    unit_spawn = models.BooleanField(default=False)
    is_sea = models.BooleanField(default=False)
    is_coast = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Locations'
    def __str__(self):
        return self.name

# the location and what is next to itself
class Next_to(models.Model):
    # not sure on on delete here
    # only one type of location but many next_tos
    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='location')
    next_to = models.ForeignKey(Location, on_delete=models.DO_NOTHING,related_name='next_to')
    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name_plural = 'Next_to'

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    can_float = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name_plural = 'Units'

class Turn(models.Model):
    year = models.IntegerField()
    is_autumn = models.BooleanField(default=False)
    def __str__(self):
        return str(self.pk)

# want the order to be kept for history, even if unit is destoryed later
class Order(models.Model):

    class MoveType(models.TextChoices):
        HOLD = 'HLD', _('Hold')
        MOVE = 'MVE' , _('Move')
        SUPPORT = 'SPT', _('Support')
        CONVOY = 'CVY', _('Convoy')

    class Meta:
        verbose_name_plural = 'Orders'

    # basic information, generated by backend first
    instruction = models.CharField(max_length=3,choices=MoveType.choices,default=MoveType.HOLD) # Not null
    turn = models.ForeignKey(Turn, on_delete=models.DO_NOTHING) # Not null
    target_unit = models.ForeignKey(Unit,on_delete=models.DO_NOTHING,related_name='target_unit') # Not null
    current_location = models.ForeignKey(Location,on_delete=models.DO_NOTHING,related_name='current_location') # Not null
    target_location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='target_location')
    # convoy operation only
    reference_unit = models.ForeignKey(Unit,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit')
    reference_unit_current_location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_current_location')
    reference_unit_new_location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_new_location')

    def __str__(self):
        return str(self.pk)
    
class Outcome(Order):
    # copy of Orders - show the orders that actually happened
    class Meta:
        proxy = True
        verbose_name_plural = 'Outcomes'
        
    def __str__(self):
        return str(self.pk)
