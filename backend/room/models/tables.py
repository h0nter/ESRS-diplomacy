from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

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
    text_pos = models.CharField(max_length=10)  
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
    class Meta:
        verbose_name_plural = 'Map_Polygons'
    def __str__(self):
        return self.pk

# the location and what is next to itself
class Next_to(models.Model):
    # not sure on on delete here
    # only one type of location but many next_tos
    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='location')
    next_to = models.ForeignKey(Location,on_delete=models.DO_NOTHING,related_name='next_to')

    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name_plural = 'Next_to'

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    can_float = models.BooleanField(default=False)

    def move(self,order):
        if(type(order) is Order):
            Unit.objects.filter(pk=self.pk).update(location=order.target_location)
        else:
            raise TypeError('Type should be Order')
    
    def __str__(self):
        return str(self.pk)
    class Meta:
        abstract = True
        verbose_name_plural = 'Units'


# Moving an actual Unit is done via the Parent Class Unit
# Calling move(order), this changes the location in the database
class Army(Unit):
    def validate_move(self)-> bool:
        return True
    
    def validate_support(self) -> bool:
        return True


class Fleet(Unit):
    def validate_move(self) -> bool:
        return True

    def validate_support(self) -> bool:
        return True

    def validate_convoy(self) -> bool:
        return True
    #         self.unit = Unit.objects.filter(pk=self.unit.pk).first()
    #         self.unit.location = self.order.target_location
    #         self.unit.save()


class Turn(models.Model):
    year = models.IntegerField()
    is_autumn = models.BooleanField(default=False)
    #build_time = models.DateTimeField(auto_now_add=True)
    #close_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.pk)
    # set the close_time while save, automatactly add 2 hours
    def save(self, *args, **kwargs):
        #self.close_time = self.build_time + datetime.timedelta(hours=2)
        super(Turn, self).save(*args, **kwargs)

class OrderManager(models.Manager):
    def validate_order_table(self):
        self.legitamise_orders()
        self.calculate_moves()
        self.evaluate_calulations()
        self.perform_operations()
        pass

    # remove orders that are theoritcally possible
    def legitamise_orders(self):
        #move
        #support
        #convoy

        # current?? - input turn number somehow
        for order in Order.objects.filter(turn='current'):
            pass
        pass

    # calculate tallies 
    def calculate_moves(self):
        # move/support
        # each location added to list and tallied
        pass

    # evalulate tallies -> put in table?
    def evaluate_calulations(self) :
        # for each calculation evaluate
        # those that fail, order cancels
        pass

    # Move Units
    def perform_operations(self):
        for successful_outcome in Outcome.objects.filter(validation=True):
            successful_outcome.order_reference.target_unit.move(successful_outcome.order_reference)
        pass

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
    target_location = models.ForeignKey(Location,blank=True,on_delete=models.DO_NOTHING,related_name='target_location')
    # convoy operation only
    reference_unit = models.ForeignKey(Unit,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit')
    reference_unit_current_location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_current_location')
    reference_unit_new_location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='reference_unit_new_location')

    def __str__(self):
        return str(self.pk)
    
class Outcome(models.Model):
    # copy of Orders - show the orders that actually happened
    order_reference = models.ForeignKey(Order,on_delete=models.DO_NOTHING,related_name='order_reference')
    validation = models.BooleanField()
    class Meta:
        # proxy = True
        verbose_name_plural = 'Outcomes'
        
    def __str__(self):
        return str(self.pk)
