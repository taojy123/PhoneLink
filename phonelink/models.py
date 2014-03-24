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
    def links(self):
        return Link.objects.filter(phone=self.phone)

    @property
    def show_phone(self):
        return self.phone

    @property
    def show_color(self):
        if self.count == 2:
            return "orange"
        if self.count == 3:
            return "green"
        if self.count == 4:
            return "blue"
        if self.count == 5:
            return "pink"
        if self.count >= 6:
            return "red"
        if Blacklist.objects.filter(phone=self.phone):
            return "black"
        return "grey"



    @property
    def remind_str(self):
        msg = ""
        if self.count > 1:
            msg += u" %d 次出现 / "%self.count
            for link in self.links:
                msg += link.person.name + " / "
        if Blacklist.objects.filter(phone=self.phone):
            msg += " <%s> "%Blacklist.objects.filter(phone=self.phone)[0].mark
        return msg


class Blacklist(models.Model):
    phone = models.CharField(max_length=64, blank=True , null=True)
    mark = models.CharField(max_length=64, blank=True , null=True)


