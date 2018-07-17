from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.db.models import Q
from transport.models import Trip, Parcel, Route, City, Location, Offer, Delivery
from comments.models import Question
from globals.models import Profile
from django.utils import timezone
import datetime
import pytz
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.timezone import get_current_timezone
import json
import traceback
# Create your views here.

def create_datetime(date, time, tz):
    h,m = time.split(':')
    time = datetime.time(hour=int(h), minute=int(m))
    date = parse_date(date)
    dt = datetime.datetime.combine(date, time)
    dt = dt.replace(tzinfo=get_current_timezone())
    #dt = dt.replace(tzinfo=datetime.timezone(datetime.timedelta(seconds=int(tz)*3600)))
    return dt

class ValidationError(Exception):
    def __init__(self, errors):
        Exception.__init__(self)
        self.errors = errors

def validate_trip(request):
    errors = {}
    print('validate_trip', request)
    _from = request['from']
    if not _from:
        errors['from']="Origin must be specified"
            
    _to=request['to']
    if not _to:
        errors['to']="Destination must be specified"
    try:
        _date=request['date']
        _time=request['time']
        due_date = create_datetime(_date, _time, +2)
    except:
        traceback.print_exc()
        errors['trip_start']='Invalid date'
        errors['time_start']='Invalid date'
        
    try:
        _date=request['date_end']
        _time=request['time_end']
        due_date = create_datetime(_date, _time, +2)
    except:
        traceback.print_exc()
        errors['trip_end']='Invalid date'
        errors['time_end']='Invalid date'

    if errors:
        raise ValidationError(errors)

    return


def add_trip(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {}
            if 'id' in request.GET:
                profile = Profile.objects.get(user=request.user)
                trip = Trip.objects.get(id=int(request.GET['id']))
                context['trip']=trip
                if trip.rider != profile:
                    return HttpResponseForbidden()
            template = loader.get_template('transport/new_trip_form.html')
            return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    elif request.method=='POST':
        try:
            validate_trip(request.POST)
        except ValidationError as ex:
            return HttpResponseServerError(json.dumps({'errors':ex.errors}), content_type="application/json")

        _from = request.POST['from']
        _to=request.POST['to']
        _date_start=request.POST['date']
        if 'date_end' in request.POST:
            _date_end=request.POST['date_end']
        else:
            _date_end = _date_start
            
        if 'time' in request.POST and ':' in request.POST['time']:
            _time_start=request.POST['time']
        else:
            _time_start = '22:00'
            
        if 'time_end' in request.POST and ':' in request.POST['time_end']:
            _time_end=request.POST['time_end']
        else:
            _time_end = '23:00'

        if 'tz' in request.POST:
            _tz = int(request.POST['tz'])/60
        else:
            _tz = +2 #use central Russia/Moscow as a default

        if 'min_price' in request.POST:
            try:
                _min_price = int(request.POST['min_price'])
            except:
                _min_price = 0
        else:
            _min_price = 0

        if 'max_weight' in request.POST:
            try:
                _max_weight = int(request.POST['max_weight'])
            except ValueError:
                _max_weight = 20
        else:
            _max_weight = 0
            
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
        ds = create_datetime(_date_start, _time_start, _tz)
        de = create_datetime(_date_end, _time_end, _tz)
        trip = Trip(start_date=ds, end_date=de)
        trip.rider=p
        trip.route=route
        trip.transport=0
        trip.duration = 0
        trip.price = _min_price
        trip.max_weight = _max_weight
        trip.save()
        if 'offer_to' in request.POST:
            request.POST['trip']=str(trip.id)
            #TODO: price
            return offer_trip(request, id=request.POST['offer_to'])
        else:
            return HttpResponseRedirect('/profile/deliveries')
        
def validate_parcel(request):
    errors = {}
    _from = request['from']
    if not _from:
        errors['from']="Origin must be specified"
            
    _to=request['to']
    if not _to:
        errors['to']="Destination must be specified"
    try:
        _date=request['date']
        _time=request['time']
        due_date = create_datetime(_date, _time, +2)
    except:
        errors['date']='Invalid date'
        errors['time']='Invalid date'

    if not request['name']:
        errors['name'] = 'Name must be specified'
        
    _weight=request['weight']

    if errors:
        raise ValidationError(errors)

    return
    

def add_parcel(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        print (request.GET)
        if request.user.is_authenticated:
            if 'id' in request.GET:
                parcel = Parcel.objects.get(id=request.GET['id'])
                if parcel.owner != profile:
                    return HttpResponseForbidden('')
                if parcel.offer_set.count() > 0:
                    print(parcel.offer_set)
                    template = loader.get_template('globals/message_popup.html')
                    context = {'message': 'Нельзя редактировать посылку с предложениями о доставке'}
                else:
                    template = loader.get_template('transport/new_parcel_form.html')
                    context = {'parcel': parcel}
                return  HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('transport/new_parcel_form.html')
                context = {}
                return  HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/auth/login')
    elif request.method == 'POST':
        print(request.POST)
        try:
            prc = validate_parcel(request.POST)
            _from = request.POST['from']
            _to=request.POST['to']
            _date=request.POST['date']
            _time=request.POST['time']
            _weight=request.POST['weight']
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

            if 'id' in request.POST and request.POST['id']!='':
                parcel = Parcel.objects.get(id=int(request.POST['id']))
                if parcel.owner!=profile:
                    return HttpResponseForbidden()
            else:
                parcel = Parcel()

            ls = Location(address="Somwhere")
            ls.city = start
            ls.save()
            le = Location(address="Somewhere")
            le.city=end
            le.save()

            parcel.description = request.POST['name']
            parcel.owner = p
            parcel.value = 100
            try:
                parcel.max_price = int(request.POST['max_price'])
            except ValueError:
                parcel.max_price = 0
            parcel.origin = ls
            parcel.destination = le
            parcel.due_date = create_datetime(_date, _time, +2)  #TODO: timezone
            parcel.comment = request.POST['descr']
            try:
                parcel.weight=int(_weight)
            except ValueError:
                parcel.weight=0
            parcel.save()
            if 'offer_for' in request.POST:
                request.POST['parcel']=str(parcel.id)
                #TODO: price
                return offer_trip(request, id=request.POST['offer_to'])
            else:
                return HttpResponseRedirect('/profile/parcels')
        except ValidationError as ex:
            return HttpResponseServerError(json.dumps({'errors':ex.errors}), content_type="application/json")
            
def trip_search(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('transport/trip_search.html')
        actual = Q(published=True, start_date__gt=timezone.now())

        if 'origin' in request.GET and request.GET['origin']!='':
            orig = Q(route__start__name=request.GET['origin'])
            origin = request.GET['origin']
        else:
            orig = Q()
            origin = ''
            
        if 'destination' in request.GET and request.GET['destination']!='':
            dest = Q(route__end__name=request.GET['destination'])
            destination = request.GET['destination']
        else:
            dest = Q()
            destination = ''
            
        if 'date' in request.GET and request.GET['date']!='' and request.GET['date']!='any':
            date = Q(end_date__lt=request.GET['date'])
            due_date = request.GET['date']
        else:
            date = Q(end_date__gt=timezone.now())
            due_date = ''

        if request.user.is_authenticated:
            p = Profile.objects.get(user=user)
            mine = Q(rider=p)
            trips = Trip.objects.filter(actual & orig & dest & date & ~mine)
        else:
            trips = Trip.objects.filter(actual & orig & dest & date)

        context = {'trips': trips, 'origin':origin, 'destination':destination, 'due_date':due_date}
        if user.is_authenticated:
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
            origin = request.GET['origin']
        else:
            orig = Q()
            origin = ''
            
        if 'destination' in request.GET and request.GET['destination']!='':
            dest = Q(destination__city__name=request.GET['destination'])
            destination = request.GET['destination']
        else:
            dest = Q()
            destination = ''

        if 'date' in request.GET and request.GET['date']!='' and request.GET['date']!='any':
            date = Q(due_date__gt=request.GET['date'])
            due_date = request.GET['date']
        else:
            date = Q(due_date__gt=timezone.now())
            due_date = ''
            
        actual = Q(delivery=None, published=True)
        
        if request.user.is_authenticated:
            p = Profile.objects.get(user=user)
            mine = Q(owner=p)
            parcels = Parcel.objects.filter(orig & dest & date & actual & ~mine)
        else:
            parcels = Parcel.objects.filter(orig & dest & date & actual)
            
        context = {'parcels': parcels, 'origin':origin, 'destination':destination, 'due_date':due_date}
        if user.is_authenticated:
            context['profile'] = p
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
        
def parcel(request, id):
    user = request.user
    if request.method=='GET':
        try:
            parcel = Parcel.objects.get(id=id)
            template = loader.get_template('transport/deal.html')
            context = {'parcel': parcel}
            if user.is_authenticated:
                profile=Profile.objects.get(user=user)
                context['profile'] = profile
                context['mine'] = parcel.owner==profile
                qs = list(Question.objects.filter(parcel=parcel))
                context['questions'] = qs
            else:
                context['profile']=None
            return  HttpResponse(template.render(context, request))
        except Parcel.DoesNotExist:
            return HttpResponseNotFound()
'''
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
'''
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
            qs = list(Question.objects.filter(parcel=parcel))
            print(qs)
            context['questions']=qs
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
            context['questions']=list(Question.objects.filter(trip=trip))
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
        return HttpResponseRedirect('/transport/parcel/{0}/deal'.format(parcel.id))

def offer_parcel(request, id):
    trip = Trip.objects.get(id=id)
    p = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        template = loader.get_template('transport/offer_parcel_form.html')
        parcels = Parcel.objects.filter(
            owner=p,
            origin__city=trip.route.start,
            destination__city=trip.route.end,
            due_date__lt=trip.end_date)
        context = {'profile':p, 'parcels':parcels, 'trip':trip}
        return  HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        parcel = Parcel.objects.get(id=int(request.POST['parcel']))
        if parcel.owner == p:
            offer = Offer()
            offer.receiver = parcel.owner
            offer.parcel = parcel
            offer.trip = trip
            offer.price = int(request.POST['price'])
            offer.save()
            parcel.owner.notify(topic='Trip offer', text='{0} offered to transport {1} for {2}'.format(p.name_public, parcel.description, offer.price))
        else:
            return HttpResponseForbidden()
        return HttpResponseRedirect('/transport/parcel/{0}'.format(parcel.id))
        #return HttpResponseRedirect('/transport/trip/{0}/deal'.format(trip.id))
