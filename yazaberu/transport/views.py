from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.db.models import Q
from transport.models import Trip, Parcel, Route, City, Location
from globals.models import Profile
from django.utils import timezone
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
        _from = request.POST['from']
        _to=request.POST['to']
        _date=request.POST['date']
        p = Profile.objects.get(user=request.user)
        try:
            route = Route.objects.get(start__name=_from, end__name=_to)
        except Route.DoesNotExist:
            #TODO: move to Route.create()
            try:
                start = City.objects.get(name = _from)
            except City.DoesNotExist:
                start = City(name=_from)
                start.save()
            try:
                end = City.objects.get(name = _to)
            except City.DoesNotExist:
                end = City(name=_to)
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
            template = loader.get_template('transport/new_parcel_form.html')
            context = {}
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    else:
        _from = request.POST['from']
        _to=request.POST['to']
        _date=request.POST['date']
        p = Profile.objects.get(user=request.user)
        try:
            start = City.objects.get(name = _from)
        except City.DoesNotExist:
            start = City(name=_from)
            start.save()
        try:
            end = City.objects.get(name = _to)
        except City.DoesNotExist:
            end = City(name=_to)
            end.save()
        ls = Location(address="Somwhere")
        ls.city = start
        ls.save()
        le = Location(address="Somewhere")
        le.city=end
        le.save()
        
        parcel = Parcel()
        parcel.description = "Something"
        parcel.owner = p
        parcel.weight = 1
        parcel.value = 123
        parcel.max_price = 101
        parcel.origin = ls
        parcel.destination = le
        parcel.due_date = _date
        parcel.comment = "Comment"
        parcel.save()
        return HttpResponse('OK')

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
            
        if 'date' in request.GET and request.GET['date']!='' and request.GET['date']!='any':
            date = Q(end_date__le=request.GET['date'])
        else:
            date = Q(end_date__gt=timezone.now())

        if request.user.is_authenticated():
            p = Profile.objects.get(user=user)
            mine = Q(rider=p)
            trips = Trip.objects.filter(orig & dest & date & ~mine)
        else:
            trips = Trip.objects.filter(orig & dest & date)

        context = {'trips': trips}
        if user.is_authenticated():
            context['profile']=p
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
            
        if 'date' in request.GET and request.GET['date']!='' and request.GET['date']!='':
            date = Q(due_date__le=request.GET['date'])
        else:
            date = Q(due_date__gt=timezone.now())
            
        actual = Q(completed=False, delivery=None, )
        
        if request.user.is_authenticated():
            p = Profile.objects.get(user=user)
            mine = Q(owner=p)
            parcels = Parcel.objects.filter(orig & dest & date & actual & ~mine)
        else:
            parcels = Parcel.objects.filter(orig & dest & date & actual)
            
        context = {'parcels': parcels}
        if user.is_authenticated():
            context['profile'] = p
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
