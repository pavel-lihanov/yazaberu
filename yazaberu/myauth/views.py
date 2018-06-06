from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.contrib.auth.models import User
from globals.models import Profile, Avatar
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

import uuid

from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from globals.social_network import providers

auth_sessions = {}

#TODO!!! login decorators
@ensure_csrf_cookie
@sensitive_post_parameters('password')
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
        
@ensure_csrf_cookie
def login_sn(request, provider):
    if request.method == 'GET':
        return  HttpResponse('Not valid', status=422)
    elif request.method == 'POST':
        if provider in providers:
            p = providers[provider]
        h = hash(request)
        auth_sessions[h] = p()
        request.session['hash'] = h
        redirect_url = auth_sessions[h].request_auth(request)
        return HttpResponse(redirect_url)
    else:
        return  HttpResponse('Not valid', status=422)
        
def done(request):
    session = auth_sessions[request.session['hash']]
    session.accept_auth(request)
    try:
        p, sn = Profile.find(session)
    except Profile.DoesNotExist:
        p, sn = session.socialnetwork_model.register_user(session)
    auth_login(request, p.user)
    return HttpResponseRedirect('/profile')

def register(request):
    if request.method == 'GET':
        template = loader.get_template('myauth/register_form.html')
        context = {}
        return  HttpResponse(template.render(context, request))
    else:
        email = request.POST['email'].strip() if 'email' in request.POST else ''
        phone = request.POST['phone'].strip() if 'phone' in request.POST else ''
        p = Profile.create(
            first_name=request.POST['first_name'].strip(),
            last_name = '',
            email = email,
            phone = phone)
        auth_login(request, p.user)
        return HttpResponseRedirect('/auth/change_password')

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
    
@sensitive_post_parameters('password')
@sensitive_post_parameters('password2')
def change_password(request):
    user = request.user
    if request.method == 'POST':
        print(request.POST)
        if user.is_authenticated() and user.has_usable_password():
            form = PasswordChangeForm(user, data=request.POST)
        else:
            form = SetPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/profile')
        else:
            print('Validation failed:', form.errors)
            return HttpResponse('Validation error', status=422)
    elif request.method == 'GET':
        print('change_password', request.GET, request.session, request.user)
        template = loader.get_template('myauth/password_change_form.html')
        context = {'has_password': user.is_authenticated() and user.has_usable_password(), 'action': '/auth/change_password'}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse('Not valid {0}'.format(request.method), status=422)
        
def reset_done(request):
    #TODO: page for reset confirm
    return HttpResponse("Reset done, please check your inbox")
    
class MyPasswordResetView(PasswordResetView):
    template_name = 'myauth/forgot_form.html'
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        print('MyPasswordResetView', self.request.GET)
        return super(MyPasswordResetView, self).get(*args, **kwargs)
        
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'myauth/reset.html'
    def form_invalid(self, form):
        return HttpResponse(json.dumps({'ok': False, 'errors': form.errors}), content_type="application/json")
        
    def form_valid(self, form):
        form.save()
        return HttpResponse('Password changed, you can now login using email and your new password')

    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        print('MyPasswordResetConfirmView', self.request.GET)
        res = super(MyPasswordResetConfirmView, self).get(*args, **kwargs)
        print(res)
        return res
        
class MyPasswordChangeView(PasswordChangeView):
    @property
    def form_class(self):
        user = self.request.user
        if user.has_usable_password():
            return PasswordChangeForm
        else:
            return SetPasswordForm
        
    def form_invalid(self, form):
        return HttpResponse("Error!")
        
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return HttpResponseRedirect('/profile')
        
    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        print('MyPasswordChangeView', self.request.GET, self.request.session, self.request.user)
        return super(MyPasswordChangeView, self).get(*args, **kwargs)


