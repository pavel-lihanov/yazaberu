from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.db.models import Q
from transport.models import Trip, Parcel, Route, City, Location, Offer, Delivery
from globals.models import Profile
from django.utils import timezone
# Create your views here.

def add_trip(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            template = loader.get_template('transport/new_trip_form.html')
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
        return HttpResponseRedirect('/profile/deliveries')
    
def add_parcel(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            template = loader.get_template('transport/new_parcel_form.html')
            context = {}
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    elif request.method == 'POST':
        print(request.POST)
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
        parcel.description = request.POST['name']
        parcel.owner = p
        parcel.weight = int(1)
        parcel.value = 100
        parcel.max_price = int(request.POST['max_price'])
        parcel.origin = ls
        parcel.destination = le
        parcel.due_date = _date
        parcel.comment = request.POST['descr']
        parcel.save()
        return HttpResponseRedirect('/profile/parcels')

def trip_search(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('transport/trip_search.html')
        actual = Q(published=True, start_date__gt=timezone.now())

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
            trips = Trip.objects.filter(actual & orig & dest & date & ~mine)
        else:
            trips = Trip.objects.filter(actual & orig & dest & date)

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
            
        if 'date' in request.GET and request.GET['date']!='' and request.GET['date']!='any':
            date = Q(due_date__lt=request.GET['date'])
        else:
            date = Q(due_date__gt=timezone.now())
            
        actual = Q(delivery=None, published=True)
        
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

def offer_trip(request, parcel):
    if request.method=='GET':
        return HttpResponse('Not valid', status=422)
    elif request.method=='POST':
        p = Profile.objects.get(user=request.user)
        parcel = parcel.objects.get(id=parcel)
        trip=request.POST['trip']
        #TODO: move to Offer.create(parcel, price) or parcel.make_offer(trip, price)
        offer = Offer()
        assert(trip.rider == p)
        offer.delivery=delivery
        offer.trip = trip
        offer.receiver = parcel.owner
        offer.save()
        return HttpResponse('OK')

def offer_parcel(request, trip):
    if request.method=='GET':
        return HttpResponse('Not valid', status=422)
    elif request.method=='POST':
        p = Profile.objects.get(user=request.user)
        trip = parcel.objects.get(id=trip)
        parcel=request.POST['parcel']
        #TODO: move to Offer.create(trip, price) or trip.make_offer(parcel, price)
        offer = Offer()
        assert(parcel.owner == p)
        offer.delivery=delivery
        offer.trip = trip
        offer.receiver = trip.rider
        offer.save()
        return HttpResponse('OK')
        
def accept_offer(request, id):
    if request.method=='GET':
        return HttpResponse('Not valid', status=422)
    elif request.method=='POST':
        p=Profile.objects.get(user=request.user)
        offer=Offer.objects.get(id=id)
        deliv = offer.accept()
        return HttpResponseRedirect('/transport/parcel/{0}'.fromat(deliv.parcel.id))

def decline_offer(request, id):
    if request.method=='GET':
        return HttpResponse('Not valid', status=422)
    elif request.method=='POST':
        p=Profile.objects.get(user=request.user)
        p_id = offer.parcel_id
        offer=Offer.objects.get(id=id)
        offer.decline()
        return HttpResponseRedirect('/transport/parcel/{0}'.fromat(p_id))

def parcel_deal(request, id):
    if request.method=='GET':
        p = Profile.objects.get(user=request.user)
        parcel = Parcel.objects.get(id=id)
        if parcel.published or parcel.owner==p:
            context = {}
            offers = parcel.offer_set.all()
            template = loader.get_template('transport/deal.html')
            context['profile']=p
            context['parcel']=parcel
            context['offers']=list(offers)
            context['questions']=list(Question.objects.get(parcel=parcel))
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponse('Not valid', status=422)

def trip_deal(request, id):
    if request.method=='GET':
        p = Profile.objects.get(user=request.user)
        trip = Trip.objects.get(id=id)
        if trip.published or trip.owner==p:
            context = {}
            offers = trip.offer_set.all()
            template = loader.get_template('transport/deal.html')
            context['profile']=p
            context['trip']=trip
            context['offers']=list(offers)
            context['questions']=list(Question.objects.get(trip=trip))
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponse('Not valid', status=422)

        
def offer_trip(request, id):
    parcel = Parcel.objects.get(id=id)
    p = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        template = loader.get_template('transport/offer_trip_form.html')
        trips = Trip.objects.filter(rider=p, route__end=parcel.destination.city, start_date__gt=timezone.now(), end_date__lt=parcel.due_date)
        context = {'profile':p, 'parcel':parcel, 'trips':trips}
        return  HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        trip = Trip.objects.get(id=int(request.POST['trip']))
        if trip.rider == p:
            offer = Offer()
            offer.receiver = parcel.owner
            offer.parcel = parcel
            offer.trip = trip
            offer.price = int(request.POST['price'])
            offer.save()
            parcel.owner.notify(topic='Trip offer', text='{0} offered to transport {1} for {2}'.format(p.name_public, parcel.description, offer.price))
        else:
            return HttpResponseForbidden()
        return HttpResponseRedirect('/transport/deal/{0}'.format(parcel.id))

def offer_parcel(request, id):
    trip = Trip.objects.get(id=id)
    p = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        template = loader.get_template('transport/offer_parcel_form.html')
        parcels = Parcel.objects.filter(
            owner=p,
            destination__city=trip.destination,
            due_date__le=trip.end_date)
        context = {'profile':p, 'parcels':parcels}
        return  HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        return HttpResponse('Not implemented', status=422)
