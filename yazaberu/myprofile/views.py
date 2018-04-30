from django.shortcuts import render
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
from django.db.models import Q

from globals.models import Profile
from django.utils import timezone

from transport.models import Delivery, Parcel, Trip
from comments.models import Message, Review

def myprofile(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/index.html')
        context = {'profile': Profile.objects.get(user=request.user)}
        return  HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        first_name = request.POST['usrname']
        last_name = request.POST['surname']
        email = request.POST['mail'].strip()
        phone = request.POST['phone'].strip()
        profile = Profile.objects.get(user=request.user)
        if first_name:
            profile.first_name = first_name
            profile.user.first_name = first_name
        if last_name:
            profile.last_name = last_name
            profile.user.last_name = last_name
            
        old_email = profile.user.email
        profile.user.email = email
        #TODO: send emails
        profile.phone = phone
        profile.user.save()
        profile.save()
        return HttpResponseRedirect('/profile/')
    else:
        return HttpResponse('Not valid', status=422)

def mydeliveries(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/deliveries.html')
        me=Profile.objects.get(user=request.user)
        all_trips = Trip.objects.filter(rider=me)
        trips = {'future': all_trips.filter(start_date__gt=timezone.now()), 'completed': all_trips.filter(end_date__lt=timezone.now())}
        context = {'profile': me, 'trips': trips}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
        
def my_delivery_list(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/delivery_list.html')
        me=Profile.objects.get(user=request.user)
        all_trips = Trip.objects.filter(rider=me)
        trips = {'future': all_trips.filter(start_date__gt=timezone.now()), 'completed': all_trips.filter(end_date__lt=timezone.now()),'draft': []}
        context = {'profile': me, 'trips': trips}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def my_parcel_list(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/parcel_list.html')
        me=Profile.objects.get(user=request.user)
        pending = Q(delivery=None) | Q(delivery__delivered=False)
        pending_parcels=Parcel.objects.filter(pending, owner=me)
        deliveries_for_me=Delivery.objects.filter(parcel__owner=me, delivered=True)
        context = {'profile': me, 'pending_parcels': pending_parcels, 'deliveries_for_me':deliveries_for_me}
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
        messages=Message.objects.filter(receiver=me)
        context = {'profile': me, 'messages':messages}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
        
def myreviews(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/reviews.html')
        me=Profile.objects.get(user=request.user)
        reviews=Review.objects.filter(message__receiver=me)
        context = {'profile': me, 'reviews':reviews}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
