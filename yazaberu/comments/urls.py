from django.conf.urls import url
from django.contrib import admin
#import transport.views
import comments.views

urlpatterns = [
    url(r'^parcel/(?P<id>[0-9]+)/ask_question$', comments.views.ask_question, name='ask_question'),
    url(r'^question/(?P<id>[0-9]+)/answer$', comments.views.answer_question, name='answer_question'),
    url(r'^delivery/(?P<id>[0-9]+)/review_driver$', comments.views.review_driver, name='review_driver'),
    url(r'^delivery/(?P<id>[0-9]+)/review_sender$', comments.views.review_sender, name='review_sender'),
    url(r'^review/(?P<id>[0-9]+)/answer$', comments.views.answer_review, name='answer_review'),
]