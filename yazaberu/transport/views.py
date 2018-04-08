from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.db.models import Q
from transport.models import Trip, Parcel, Route, City
from globals.models import Profile

# Create your views here.

def add_trip(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            template = loader.get_template('transport/add_trip_form.html')
            context = {}
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    elif request.method=='POST':
        print(request.POST)
        _from = request.POST['from']
        _to=request.POST['to']
        _date=request.POST['date']
        p = Profile.objects.get(user=request.user)
        try:
            route = Route.objects.get(start__name=_from, end__name=_to)
        except Route.DoesNotExist:
            #TODO: move to Route.create()
            try:
                start = City.objects.get(name = _start)
            except City.DoesNotExist:
                start = City(name=_start)
                start.save()
            try:
                end = City.objects.get(name = _end)
            except City.DoesNotExist:
                end = City(name=_end)
                end.save()
            route = Route(start=start, end=end)
            route.save()

        trip = Trip(start_date=_date, end_date=_date)
        trip.rider=p
        trip.route=route
        trip.transport=0
        trip.duration = 0
        trip.save()
        return HttpResponse('OK')
    
def add_parcel(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            template = loader.get_template('transport/add_parcel.html')
            context = {}
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    else:
        return HttpResponse('Not valid', status=422)

def trip_search(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('transport/trip_search.html')
        if 'origin' in request.GET and request.GET['origin']!='':
            orig = Q(route__start__name=request.GET['origin'])
        else:
            orig = Q()
            
        if 'destination' in request.GET and request.GET['destination']!='':
            dest = Q(route__end__name=request.GET['destination'])
        else:
            dest = Q()
            
        #TODO: date
        trips = Trip.objects.filter(orig & dest)
        context = {'trips': trips}
        if user.is_authenticated():
            context['profile']=Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
    
def parcel_search(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('transport/parcel_search.html')
        if 'origin' in request.GET  and request.GET['origin']!='':
            orig = Q(origin__city__name=request.GET['origin'])
        else:
            orig = Q()
            
        if 'destination' in request.GET and request.GET['destination']!='':
            dest = Q(destination__city__name=request.GET['destination'])
        else:
            dest = Q()
            
        #TODO: date
        parcels = Parcel.objects.filter(orig & dest)
        context = {'parcels': parcels}
        if user.is_authenticated():
            context['profile']=Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
        
def parcel(request, id):
    if request.method=='GET':
        try:
            parcel = Parcel.objects.get(id=id)
            template = loader.get_template('transport/deal.html')
            context = {'parcel': parcel}
            if user.is_authenticated():
                profile=Profile.objects.get(user=user)
                context['profile']=profile
                context['mine']=parcel.owner==profile
            else:
                context['profile']=None
            return  HttpResponse(template.render(context, request))
        except Parcel.DoesNotExist:
            return HttpResponseNotFound()
