from django.db import models
from room.models.locations import Country, Location

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    can_float = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Units'
    def __str__(self):
        return str(self.pk)

    def move(self,location):
        if(type(location) is Location):
            #thisUnit = Unit.objects.get(pk=self.pk)
            self.location = location
            self.save()
        else:
            raise TypeError('Type should be Location')
