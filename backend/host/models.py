from django.db import models
from django.utils.translation import gettext_lazy as _


# status for each room
class Host(models.Model):
    class StatusType(models.TextChoices):
        Initial = 'Init', _('Initial')
        Opening = 'Open', _('Opening')
        Waiting = 'Wait' , _('Waiting')
        Checking = 'Check', _('Checking')
        Closing = 'Close', _('Closing')

    total_user = models.IntegerField(default=1)
    alive_user = models.IntegerField(default=1)
    location_num = models.IntegerField()
    room_status = models.CharField(max_length=5,choices=StatusType.choices,default=StatusType.Initial)
    
    class Meta:
        verbose_name_plural = 'Host'

    def __str__(self):
        return str(self.pk)


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length= 30, unique=True)
    cookies = models.CharField(max_length= 32, unique=True)
    room = models.ForeignKey(Host,on_delete=models.CASCADE)
