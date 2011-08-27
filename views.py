# Copyright 2011 Theodore Boyd
import cgi
import datetime
import urllib

import models
import utils

from google.appengine.ext import db
from google.appengine.api import users

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError


def Home(request):
  return render_to_response('home.html', {})
    

def GuestbookView(request):
  greetings_query = models.Greeting.all().order('-date')
  greetings = greetings_query.fetch(10)

  if users.get_current_user():
    login_url = users.create_logout_url(request.get_full_path())
    login_linktext = 'Logout'
  else:
    login_url = users.create_login_url(request.get_full_path())
    login_linktext = 'Login to sign guestbook'

  template_values = {
      'greetings': greetings,
      'login_url': login_url,
      'login_linktext': login_linktext,
      'user': users.get_current_user(),
      'is_admin': users.get_current_user() == 'admin',
  }
  return render_to_response('guestbook_view.html', template_values)


def GuestbookSign(request):
  # We set the same parent key on the 'Greeting' to ensure each greeting is in
  # the same entity group. Queries across the single entity group will be
  # consistent. However, the write rate to a single entity group should
  # be limited to ~1/second.
  greeting = models.Greeting()

  if users.get_current_user():
    greeting.author = users.get_current_user()

  greeting.content = request.POST['content']
  greeting.put()
  return HttpResponseRedirect('/guestbook/view/')


def GuestbookDeleteEntry(request, key=None):
  if key:
    greeting = models.Greeting.get(key)
    greeting.delete()
  return HttpResponseRedirect('/guestbook/view/')
