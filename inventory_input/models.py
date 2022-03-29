from pyexpat import model
from statistics import mode
from django.db import models

class List(models.Model):
    pass
# Create your models here.
class Item(models.Model):
    text = models.TextField(default='', null=True)
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE, null=True)