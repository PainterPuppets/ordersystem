#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Dish(models.Model):
    dishname =  models.CharField(max_length=150)
    dimage = models.ImageField(default='/home/liqingqing/图片/1.jpg')
    fprice = models.FloatField()
    dtype = models.CharField(max_length=150)
    description = models.TextField()
    recipe = models.TextField()
    sales = models.IntegerField(default=0)


class Img(models.Model):
    name = models.CharField(max_length = 128)
    description = models.TextField()
    img = models.ImageField()
    dish = models.ForeignKey(Dish)
