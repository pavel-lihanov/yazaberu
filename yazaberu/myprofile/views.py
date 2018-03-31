from django.shortcuts import render
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
from django.db.models import Q

from globals.models import Profile

from transport.models import Delivery, Parcel

def myprofile(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/index.html')
        context = {'profile': Profile.objects.get(user=request.user)}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def mydeliveries(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/deliveries.html')
        me=Profile.objects.get(user=request.user)
        delivs = Delivery.objects.get(trip__rider=me)
        context = {'profile': me, 'deliveries': delivs}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def myparcels(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/parcels.html')
        me=Profile.objects.get(user=request.user)
        pending = Q(delivery=None) | Q(delivery__delivered=False)
        pending_parcels=Parcel.objects.filter(pending, owner=me)
        deliveries_for_me=Delivery.objects.filter(parcel__owner=me, delivered=True)
        context = {'profile': me, 'pending_parcels': pending_parcels, 'deliveries_for_me':deliveries_for_me}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def mymessages(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/messages.html')
        me=Profile.objects.get(user=request.user)
        context = {'profile': me}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
