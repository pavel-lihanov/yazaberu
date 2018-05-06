from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader

from django.utils.translation import activate, check_for_language, get_language
from django.utils.translation import ugettext as _

from django.views.static import serve
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os
from requests_oauthlib import OAuth2Session

import json
import codecs

from globals.models import GooglePlus, Facebook, Vkontakte

class AuthProvider:
    def __init__(self):
        self.socialnetwork = self.socialnetwork_model()

#for testing on localhost
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
class GoogleAuth(AuthProvider):
    client_id = '106930731650-sh2hbnmqb2i7fhe5nfndqlqaemoce2sj.apps.googleusercontent.com'
    client_secret = 'fvershdSUSCI2V8WlgiqfJ6a'
    scope = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url = "https://www.googleapis.com/oauth2/v4/token"
    redirect_uri = settings.OAUTH_REDIRECT_URI
    socialnetwork_model = GooglePlus

    def request_auth(self, request):
        self.session = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_uri)
        authorization_url, state = self.session.authorization_url(self.authorization_base_url, 
            access_type="offline", 
            prompt="select_account")
        return authorization_url
        
    def accept_auth(self, request):
        redirect_response = request.build_absolute_uri()
        self.session.fetch_token(self.token_url, client_secret=self.client_secret,
                authorization_response=redirect_response)
        r = self.session.get('https://www.googleapis.com/oauth2/v1/userinfo')
        self.info = json.loads(codecs.decode(r.content,'utf8'))
        
    @property
    def first_name(self):
        return self.info['given_name'].strip()
        
    @property
    def last_name(self):
        return self.info['family_name'].strip()
    
    @property
    def email(self):
        return self.info['email'].strip()
        
    @property
    def avatar(self):
        return {'url': self.info['picture'].strip()}
        
class VKAuth(AuthProvider):
    class Permissions:
        notify = 1
        friends = 2
        photos = 4
        audio = 8
        video = 16
        stories = 64
        pages = 128
        link = 256
        status = 1024
        notes = 2048
        messages = 4096
        wall = 8192
        ads = 32768
        offline = 65536
        docs = 131072
        groups = 262144
        notifications = 524288
        stats = 1048576
        email = 4194304
        market = 134217728
        nohttps = 0

    icon = '/static/files/vk-oauth.svg'
    redirect_uri = settings.OAUTH_REDIRECT_URI
    socialnetwork_model = Vkontakte
    authorization_base_url='https://oauth.vk.com/authorize'
    client_id = 'gGqr9ilxU9UKttGvkUsz'
    client_secret = ''
    scope = str(Permissions.notify + Permissions.offline)
    response_type = 'code'
    version='5.74'
    
    def request_auth(self, request):
        self.session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        authorization_url, state = self.session.authorization_url(self.authorization_base_url)
        return authorization_url

    def accept_auth(self, request):
        redirect_response = request.build_absolute_uri()
        '''https://oauth.vk.com/access_token?  
        client_id=APP_ID&  
        client_secret=APP_SECRET&  
        code=7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a&  
        redirect_uri=REDIRECT_URI'''
        code = request['code']
        r = self.session.get('https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri={3}'.format(self.client_id, self.client_secret, code, self.redirect_uri))
        self.info = json.loads(codecs.decode(r.content,'utf8'))
        self.access_token = self.info['access_token']
        selif.user_id = self.info['user_id']
        #self.session.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=redirect_response)
        #r = self.session.get('https://graph.facebook.com/me?fields=first_name,last_name,email,picture,link')
        #self.info = json.loads(codecs.decode(r.content,'utf8'))


class FacebookAuth(AuthProvider):
    icon = '/static/files/fb-oauth.svg'
    client_id = '146652102687184'
    client_secret = '0fa9ef9fbbccb2bd1fed14c215272989'
    scope = ["public_profile", "email"]
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = settings.OAUTH_REDIRECT_URI
    socialnetwork_model = Facebook

    def request_auth(self, request):
        from requests_oauthlib.compliance_fixes import facebook_compliance_fix
        self.session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        self.session = facebook_compliance_fix(self.session)

        authorization_url, state = self.session.authorization_url(self.authorization_base_url)
        return authorization_url
        
    def accept_auth(self, request):
        redirect_response = request.build_absolute_uri()
        self.session.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=redirect_response)
        r = self.session.get('https://graph.facebook.com/me?fields=first_name,last_name,email,picture,link')
        self.info = json.loads(codecs.decode(r.content,'utf8'))
       
    @property
    def first_name(self):
        return self.info['first_name'].strip()
        
    @property
    def last_name(self):
        return self.info['last_name'].strip()
    
    @property
    def email(self):
        return self.info['email'].strip()

    @property
    def avatar(self):
        return {'url': self.info['picture']['data']['url'].strip()}

providers = {
    'google': GoogleAuth, 
    'facebook': FacebookAuth,
    'vkontakte': VKAuth
    }
