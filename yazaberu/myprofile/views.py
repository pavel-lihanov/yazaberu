from django.shortcuts import render
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from globals.models import Profile

def myprofile(request):
    if request.method == 'GET':
        template = loader.get_template('myprofile/index.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

# Create your views here.
