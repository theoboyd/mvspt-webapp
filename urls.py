# Copyright 2011 Theodore Boyd
import settings
import views

from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # Framework
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),

    # Pages
    (r'^guestbook/sign/$', views.GuestbookSign),
    (r'^guestbook/view/$', views.GuestbookView),
    (r'^guestbook/delete/(?P<key>[a-zA-Z0-9_.-]+)/$', views.GuestbookDeleteEntry),
)
