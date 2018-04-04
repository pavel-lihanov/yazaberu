from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
import globals.models
import transport.models

def landing(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('globals/landing.html')
        routes = transport.models.get_popular_routes()
        delivered = transport.models.get_advert_delivered()
        context = {'routes':routes, 'delivered': delivered}
        if user.is_authenticated():
            context['profile']=globals.models.Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def landing_sender(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('globals/landing_sender.html')
        delivered = transport.models.get_advert_delivered()
        context = {'delivered': delivered}
        if user.is_authenticated():
            context['profile']=globals.models.Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def landing_rider(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('globals/landing_rider.html')
        context = {
            'count_waiting_parcels': transport.models.waiting_parcels_count(),
            'count_riders': transport.models.riders_count(),
            'count_delivered_parcels': transport.models.delivered_parcels_count(),
            'total_income': transport.models.total_income()
        }
        if user.is_authenticated():
            context['profile']=globals.models.Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
