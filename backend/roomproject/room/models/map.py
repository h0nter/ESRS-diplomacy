from django.db import models


class Map(models.Model):
    name = models.CharField(max_length=30)
    max_countries = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Maps'

    def __str__(self):
        return '' + self.name