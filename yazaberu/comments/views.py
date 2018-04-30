from globals.models import Profile
from transport.models import Parcel, Trip
from comments.models import Question, Message, Review

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
        text = request.POST['text']
        msg = Message()
        msg.author = profile
        msg.receiver = message.author
        msg.text = text
        msg.reply_to = message
        msg.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('Not valid', status=422)

#url(r'^question/(?P<id>[0-9]+)/answer$', comments.views.answer_question, name='answer_question'),
#url(r'^delivery/(?P<id>[0-9]+)/review_driver$', comments.views.review_driver, name='review_driver'),
#url(r'^delivery/(?P<id>[0-9]+)/review_sender$', comments.views.review_sender, name='review_sender'),

#url(r'^review/(?P<id>[0-9]+)/answer$', comments.views.answer_review, name='answer_review'),
def answer_review(request, id):
    profile = Profile.objects.get(user=request.user)
    review = Review.objects.get(id=id)
    if request.method == 'GET':
        template = loader.get_template('comments/reply_form.html')
