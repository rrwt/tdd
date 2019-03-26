from django.db import models


class List(models.Model):
    pass


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default='', on_delete=models.CASCADE)
