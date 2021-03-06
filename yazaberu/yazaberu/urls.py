"""yazaberu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import myauth.views
import globals.views
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('myauth.urls')),
    url(r'^transport/', include('transport.urls')),
    url(r'^profile/', include('myprofile.urls')),
    url(r'^comments/', include('comments.urls')),
    #dev server only
    url(r'^media/(?P<path>.*)$', serve, {'document_root': './media'}),
    url(r'^send/$', globals.views.landing_sender),
    url(r'^deliver/$', globals.views.landing_rider),
    url(r'^city$', globals.views.city_search),
    url(r'^$', globals.views.landing),
    url(r'^user/(?P<id>[0-9]+)$', globals.views.user_view),
    url(r'^avatar/(?P<id>[0-9]+)/upload$', globals.views.upload_avatar),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
