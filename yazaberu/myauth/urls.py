from django.conf.urls import url
from django.contrib import admin
import myauth.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/(?P<provider>[a-z]+)$', myauth.views.login_sn , name='login_sn'),
    url(r'^done$', myauth.views.done , name='login_sn_done'),
    url(r'^login$', myauth.views.login , name='login'),
    url(r'^register$', myauth.views.register , name='register'),
    url(r'^confirm$', myauth.views.confirm , name='confirm'),
    url(r'^welcome$', myauth.views.welcome , name='welcome'),
    url(r'^logout$', myauth.views.logout , name='logout'),
    url(r'^change_password$', myauth.views.change_password, name='change_pass'),
    
    url(r'^accounts/password_change/$', myauth.views.MyPasswordChangeView.as_view(template_name='myauth/password_change_form.html')),
    url(r'^accounts/password_change_done/$', auth_views.PasswordChangeDoneView.as_view(template_name='myauth/password_change_done.html')),
    url(r'^accounts/password_reset/$', myauth.views.MyPasswordResetView.as_view(template_name='myauth/forgot.html')),
    url(r'^accounts/password_reset_confirm/$', auth_views.PasswordResetConfirmView.as_view(template_name='myauth/password_reset_confirm.html')),
    url(r'^accounts/password_reset_done/$', auth_views.PasswordResetDoneView.as_view(template_name='myauth/password_reset_done.html')),
    url(r'^accounts/password_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='myauth/password_reset_copmlete.html')),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        myauth.views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^forgot/$', myauth.views.MyPasswordResetView.as_view(template_name='myauth/forgot_form.html')),
    url(r'^reset_done/$', myauth.views.reset_done, name='password_reset_done')
]
