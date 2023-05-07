from django.db import models
from django.utils.translation import gettext_lazy as _
from room.game.outcomeManager import OutcomeManager
from .order import Order


class OutcomeType(models.TextChoices):
        MAYBE = 'MYBE', _('Order Not Evaluated')
        MARK = 'MARK', _('Order Marked for future Evaluation')
        NO_CONVOY = 'NCVY', _('Move Order has No Convoy')
        PASS = 'PASS', _('Order Passed')
        VOID = 'VOID' , _('Order Failed')
        CUT = 'CUT', _('Order Cut')
        BOUNCE = 'BNCE', _('Order Bounced with another')
        DISLODGED = 'DLGE', _('Order Unit Dislodged')
        DISRUPTED = 'DRPT', _('Convoy Order Distrupted')
        DISBAND = 'DBAN', _('Order Unit needs to Disband')

class Outcome(models.Model):
    # copy of Orders - show the orders that actually happened
    objects = OutcomeManager()
    order_reference = models.ForeignKey(Order,on_delete=models.DO_NOTHING,related_name='outcome_reference_to_order')
    validation = models.CharField(max_length=4,choices=OutcomeType.choices,default=OutcomeType.MAYBE) # Not null
    class Meta:
        # proxy = True
        verbose_name_plural = 'Outcomes'
        
    def __str__(self):
        return str(self.pk)
