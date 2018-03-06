from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

def login(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/login.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def welcome(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/welcome.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def register(request):
    return HttpResponse('Not valid', status=422)

def forgot(request):
    return HttpResponse('Not valid', status=422)

def login_using(request, provider):
    return HttpResponse('Not valid', status=422)
