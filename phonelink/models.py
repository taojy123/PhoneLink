# -*- coding: utf-8 -*-

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=64, blank=True , null=True)


class Call(models.Model):
    person = models.ForeignKey(Person)
    time = models.CharField(max_length=64, blank=True , null=True)
    phone = models.CharField(max_length=64, blank=True , null=True)


class Link(models.Model):
    person = models.ForeignKey(Person)
    phone = models.CharField(max_length=64, blank=True , null=True)



