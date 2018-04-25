from globals.models import Profile
from transport.models import Parcel, Trip
from comments.models import Question, Message

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.template import loader


# Create your views here.

def ask_question(request, id):
    profile = Profile.objects.get(user=request.user)
    parcel = parcel.objects.get(id=id)
    if request.method=='GET':
        template = loader.get_template('comments/ask_question_form.html')
        context = {'profile': profile}
        return  HttpResponse(template.render(context, request))
    elif request.method=='POST':
        pass
    else:
        return HttpResponse('Not valid', status=422)
        
def reply(request, id):
    profile = Profile.objects.get(user=request.user)
    message = Message.objects.get(id=id)
    if request.method=='GET':
        template = loader.get_template('comments/reply_form.html')
        context={'profile': profile, 'message': message}
        return  HttpResponse(template.render(context, request))
    elif request.method=='POST':
        pass
    else:
        return HttpResponse('Not valid', status=422)
