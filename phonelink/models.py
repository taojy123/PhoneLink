# -*- coding: utf-8 -*-

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=64, blank=True , null=True)

    @property
    def links(self):
        return Link.objects.filter(person=self)

    @property
    def calls(self):
        return Call.objects.filter(person=self)


class Call(models.Model):
    person = models.ForeignKey(Person)
    time = models.CharField(max_length=64, blank=True , null=True)
    phone = models.CharField(max_length=64, blank=True , null=True)


class Link(models.Model):
    person = models.ForeignKey(Person)
    phone = models.CharField(max_length=64, blank=True , null=True)

    @property
    def count(self):
        return Link.objects.filter(phone=self.phone).count()

    @property
    def show_phone(self):
        return self.phone[:3] + "**" + self.phone[5:]

    @property
    def remind_str(self):
        msg = ""
        if self.count > 1:
            msg += " %d 次出现 "%self.count
        if Blacklist.objects.filter(phone=self.phone):
            msg += " <%s> "%Blacklist.objects.filter(phone=self.phone)[0].mark
        return msg


class Blacklist(models.Model):
    phone = models.CharField(max_length=64, blank=True , null=True)
    mark = models.CharField(max_length=64, blank=True , null=True)


