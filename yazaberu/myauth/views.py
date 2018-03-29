from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.contrib.auth.models import User
from globals.models import Profile
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/login.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        id=request.POST['id'].strip()
        print('Login, id="{0}"'.format(id))
        passwd = request.POST['password'].strip()
        try:
            print('Users:', [u.email for u in User.objects.all()])
            user = User.objects.get(email=id)
            u = authenticate(request, username=user.username, password=passwd)
            if u:
                print('Logging in')
                auth_login(request, u)
                profile = Profile.objects.get(user=u)
                return HttpResponseRedirect('/profile')
                #TODO: redirect to profile page after login
                #return do_welcome(request, profile=profile)
            else:
                return HttpResponseForbidden('Invalid password')
        except User.DoesNotExist:
            print('User not found', id)
            return HttpResponseNotFound('User not found')
        return HttpResponse('Not valid', status=422)

def welcome(request):
    if request.method == 'GET':
        return do_welcome(request, profile=Profile.objects.get(user=request.user))
    else:
        return HttpResponse('Not valid', status=422)
        
def do_welcome(request, profile):
    template = loader.get_template('myauth/welcome.html')
    context = {}
    return  HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/register.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid', status=422)

def confirm(request):
    return HttpResponse('Not valid', status=422)
        
def forgot(request):
    return HttpResponse('Not valid', status=422)

def login_using(request, provider):
    return HttpResponse('Not valid', status=422)
