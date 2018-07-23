from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
import globals.models
import transport.models
import json

def landing(request):
    if request.method == 'GET':
        user = request.user
        template = loader.get_template('globals/landing.html')
        routes = transport.models.get_popular_routes()
        delivered = transport.models.get_advert_delivered()
        context = {'routes':routes, 'delivered': delivered}
        if user.is_authenticated:
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
        if user.is_authenticated:
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
        if user.is_authenticated:
            context['profile']=globals.models.Profile.objects.get(user=user)
        else:
            context['profile']=None
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)
        
def user_view(request, id):
    if request.method == 'GET':
        u = globals.models.Profile.objects.get(id=id)
        template = loader.get_template('globals/user.html')
        context={'user': u}
        if request.user.is_authenticated:
            context['profile']=globals.models.Profile.objects.get(user=request.user)
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

from django.forms import ModelForm

class AvatarForm(ModelForm):
    class Meta:
        model = globals.models.Avatar
        fields = ['id', 'image']

def upload_avatar(request, id):
    if request.method == 'GET':
        return HttpResponse('Not valid', status=422)
    elif request.method=='POST':
        profile = globals.models.Profile.objects.get(user=request.user)
        avatar = globals.models.Avatar.objects.get(id=id)
        assert(profile.avatar==avatar)
        f=request.FILES
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            #if avatar.image:
            #    avatar.image.delete()
            #    avatar.save()
            avatar = form.save()
            print(avatar.image)
        else:
            return HttpResponseServerError('Not valid')
        return HttpResponseRedirect('/profile')
        
def city_search(request):
    if request.method == 'GET':
        search = request.GET['search']
        cities = transport.models.City.objects.filter(name__istartswith=search.capitalize())
        return HttpResponse(json.dumps([c.name for c in cities]), content_type="application/json")