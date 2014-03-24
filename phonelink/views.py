# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import os
import uuid
import xlrd


def index(request):
    return render_to_response('index.html', locals())


def get_data(request):
    print "+++++++++++++++"
    if not os.path.exists('data'):
        os.makedirs('data')

    names = os.listdir("data")
    print names
    for name in names:
        filename = "data/" + name
        name = name.split(".")[0].decode("gbk")
        print name

        if not Person.objects.filter(name=name):
            person = Person()
            person.name = name
            person.save()
        else:
            person = Person.objects.filter(name=name)[0]

        f = xlrd.open_workbook(filename)
        table = f.sheet_by_index(0)
        #times = table.col_values(1)[1:]
        phones = table.col_values(0)[1:]
        #for time, phone in zip(times, phones):
        
        for phone in phones:

            #call = Call()
            #call.person = person
            #call.time = time
            #call.phone = phone
            #call.save()

            try:
                phone = phone.strip()
            except:
                pass
            phone = str(phone).replace(".0", "")
            phone = phone.replace("'", "").replace('"', '')

            if not Link.objects.filter(person=person).filter(phone=phone):
                link = Link()
                link.person = person
                link.phone = phone
                link.save()

    t = []
    persons = Person.objects.all()
    for person in persons:
        if person.name in t:
            print "del person - ", person.name
            person.delete()
            Link.objects.filter(person=person).delete()
        t.append(person.name)

    t = []
    links = Link.objects.all()
    for link in links:
        if [link.person.id, link.phone] in t:
            print "del link - ", link.person.name
            link.delete()
        t.append([link.person.id, link.phone])

    return HttpResponseRedirect("/data")



def data(request):
    persons = Person.objects.all()
    return render_to_response('data.html', locals())




def blacklist(request):
    rs = Blacklist.objects.all()
    return render_to_response('blacklist.html', locals())


def add_blacklist(request):
    phone = request.REQUEST.get("phone")
    mark = request.REQUEST.get("mark")
    b = Blacklist()
    b.phone = phone
    b.mark = mark
    b.save()
    return HttpResponseRedirect("/blacklist")

def del_blacklist(request):
    id = request.REQUEST.get("id")
    Blacklist.objects.filter(id=id).delete()
    return HttpResponseRedirect("/blacklist")


def clean_data(request):
    Link.objects.all().delete()
    Person.objects.all().delete()
    return HttpResponseRedirect("/")




















#====================login=============================================
def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return HttpResponseRedirect("/admin/")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/admin/")
#======================================================================
