# Copyright 2011 Theodore Boyd
import settings
import views

from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # Framework
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),

    # Pages
    (r'^comments/add/$', views.CommentsAdd),
    (r'^comments/view/$', views.CommentsView),
    (r'^comments/delete/(?P<key>[a-zA-Z0-9_.-]+)/$', views.CommentsDelete),
    (r'^postings/fetch/$', views.PostingsFetch),
    (r'^postings/view/$', views.PostingsView),
    (r'^postings/delete/(?P<key>[a-zA-Z0-9_.-]+)/$', views.PostingsDelete),
    (r'^scores/add/$', views.ScoresAdd),
    (r'^scores/view/$', views.ScoresView),
    (r'^scores/delete/(?P<key>[a-zA-Z0-9_.-]+)/$', views.ScoresDelete),
    (r'^leaders/view/$', views.LeadersView),
    (r'^/$', views.Home),
    (r'^$', views.Home),
)
