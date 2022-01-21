from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')