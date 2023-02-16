from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=30)
    is_sea = models.BooleanField()
    class Meta:
        verbose_name_plural = 'Locations'
    def __str__(self):
        return self.name

class Units(models.Model):
    belong = models.CharField(max_length=30)
    position = models.ForeignKey(Location, on_delete=models.CASCADE)
    can_float = models.BooleanField()
    class Meta:
        verbose_name_plural = 'Units'
    

class Next_to(models.Model):
    next_to = models.ForeignKey(Location)
