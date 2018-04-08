from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.contrib.auth.models import User
from globals.models import Profile, Avatar
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

import uuid

#TODO!!! login decorators
def login(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/login_form.html')
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
            else:
                return HttpResponseForbidden('Invalid password')
        except User.DoesNotExist:
            print('User not found', id)
            return HttpResponseNotFound('User not found')
        return HttpResponse('Not valid', status=422)

def register(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/register_form.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        first_name=request.POST['first_name'].strip()
        phone=request.POST['phone'].strip()
        email=request.POST['email'].strip()
        u = User()
        u.username = str(uuid.uuid4())
        u.first_name = first_name
        u.email = email
        u.save()
        a = Avatar()
        a.save()
        p=Profile()
        p.first_name = first_name
        p.user = u
        p.avatar = a
        p.phone = phone
        p.save()
        auth_login(request, u)
        return do_welcome(request, p)

        
def welcome(request):
    if request.method == 'GET':
        return do_welcome(request, profile=Profile.objects.get(user=request.user))
    else:
        return HttpResponse('Not valid', status=422)
        
def do_welcome(request, profile):
    template = loader.get_template('myauth/welcome_form.html')
    context = {}
    return  HttpResponse(template.render(context, request))

def confirm(request):
    return HttpResponse('Not valid', status=422)
        
def forgot(request):
    return HttpResponse('Not valid', status=422)

def login_using(request, provider):
    return HttpResponse('Not valid', status=422)
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')