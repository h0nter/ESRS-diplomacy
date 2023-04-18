from django.db import models
from django.utils.translation import gettext_lazy as _
from room.models.locations import Location
from room.game.unitTypes import Unit
from room.game.orderManager import OrderManager

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

# want the order to be kept for history, even if unit is destoryed later
class Order(models.Model):

    class MoveType(models.TextChoices):
        HOLD = 'HLD', _('Hold')
        MOVE = 'MVE' , _('Move')
        SUPPORT = 'SPT', _('Support')
        CONVOY = 'CVY', _('Convoy')

    class Meta:
        verbose_name_plural = 'Orders'


    objects = OrderManager()
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
    
class Outcome(models.Model):
    # copy of Orders - show the orders that actually happened
    class OutcomeType(models.TextChoices):
        MAYBE = 'MYBE', _('Order Not Evaluated')
        PASS = 'PASS', _('Order Passed')
        VOID = 'VOID' , _('Order Failed')
        CUT = 'CUT', _('Order Cut')
        BOUNCE = 'BNCE', _('Order Bounced with another')
        DISLODGED = 'DLGE', _('Order Unit Dislodged')
        DISRUPTED = 'DRPT', _('Convoy Order Distrupted')
        DISBAND = 'DBAN', _('Order Unit needs to Disband')
        
    order_reference = models.ForeignKey(Order,on_delete=models.DO_NOTHING,related_name='order_reference')
    validation = models.CharField(max_length=4,choices=OutcomeType.choices,default=OutcomeType.MAYBE) # Not null
    class Meta:
        # proxy = True
        verbose_name_plural = 'Outcomes'
        
    def __str__(self):
        return str(self.pk)
