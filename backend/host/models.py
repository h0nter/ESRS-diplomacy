from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length= 30, unique=True)
    cookies = models.CharField(max_length= 32, unique=True)