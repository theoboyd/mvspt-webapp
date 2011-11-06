# Copyright 2011 Theodore Boyd
import cgi
import datetime
import logging
import re
import urllib

import models
import settings
from utils.BeautifulSoup import BeautifulSoup

from google.appengine.ext import db
from google.appengine.api import users

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError


ADMIN_EMAIL = 'theoboyd@gmail.com'


def UserInfo(path):
  '''Returns auth user info'''
  if users.get_current_user():
    login_url = users.create_logout_url(path)
    login_linktext = 'Sign out'
  else:
    login_url = users.create_login_url(path)
    login_linktext = 'Sign in'

  user = users.get_current_user()
  try:
    is_admin = users.get_current_user().email() == ADMIN_EMAIL
  except AttributeError:
    is_admin = False
    user = ''

  return {'login_url': login_url,
          'login_linktext': login_linktext,
          'user': user,
          'is_admin': is_admin}


def Home(request):
  template_values = {
      'home_active': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('home.html', template_values)


def CommentsView(request):
  comments_query = models.Comment.all().order('date')
  comments = comments_query.fetch(10)

  template_values = {
      'comments': comments,
      'comments_active': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('comments_view.html', template_values)


def CommentsAdd(request):
  comment = models.Comment()

  if users.get_current_user():
    comment.author = users.get_current_user()

  comment.content = request.POST['content']
  comment.put()
  return HttpResponseRedirect('/comments/view/')


def CommentsDelete(request, key=None):
  if key:
    comment = models.Comment.get(key)
    comment.delete()
  return HttpResponseRedirect('/comments/view/')


def PostingsFetch(unused_request):
  _GetPostingPage(1)

  return HttpResponseRedirect('/postings/view/')


def _GetPostingPage(page_num):
  url = urllib.urlopen(settings.SOURCE_ALL_URL + str(page_num))
  data = BeautifulSoup(url.read())
  postings = data.findAll('li', {'class': re.compile('hlisting')})

  for posting in postings:
    posting_object = models.Posting()
    try:
      descr_div = BeautifulSoup(posting).findAll('div', {'class': re.compile('description')})[0]
    except TypeError:
      continue
    descr_div = descr_div.findAll('h3')[0]
    description = BeautifulSoup(descr_div).findAll('a')[0]
    url = BeautifulSoup(descr_div).get('href')
    posting_object.content = posting
    logging.critical(description)
    logging.critical(url)
    #posting_object.put()


def PostingsView(request):
  postings_query = models.Posting.all().order('-date')
  postings = postings_query.fetch(100)

  template_values = {
      'postings': postings,
      'postings_active': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('postings_view.html', template_values)


def PostingsDelete(request, key=None):
  if key:
    posting = models.Posting.get(key)
    posting.delete()
  return HttpResponseRedirect('/postings/view/')


def ScoresView(request):
  scores_query = models.Score.all().order('-date')
  scores = scores_query.fetch(100)

  template_values = {
      'scores': scores,
      'scores_active': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('scores_view.html', template_values)


def ScoresAdd(request):
  score = models.Score()

  if users.get_current_user():
    score.player = models.Human()
    score.player.name = str(users.get_current_user())
  else:
    score.player = models.Computer(name="Computer 1")

  my_action = request.POST['action']

  # Dummy score-calculator:
  opp_action = my_action
  if my_action == 'Cooperate' and opp_action == 'Cooperate':
    my_score = 3
    opp_score = 3
  elif my_action == 'Cooperate' and opp_action == 'Defect':
    my_score = 0
    opp_score = 5
  elif my_action == 'Defect' and opp_action == 'Cooperate':
    my_score = 5
    opp_score = 0
  elif my_action == 'Defect' and opp_action == 'Defect':
    my_score = 1
    opp_score = 1
  score.value = my_score

  score.action = my_action.lower()
  score.put()
  return HttpResponseRedirect('/scores/view/')


def ScoresDelete(request, key=None):
  if key:
    score = models.Score.get(key)
    score.delete()
  return HttpResponseRedirect('/scores/view/')


def LeadersView(request):
  leaders_query = models.Score.all().order('-value')
  leaders = leaders_query.fetch(100)

  template_values = {
      'leaders': leaders,
      'leaders_active': True,
      'submit_disabled': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('leaders_view.html', template_values)


def LeadersAdd(request):
  leader = models.Leader()

  if users.get_current_user():
    leader.author = users.get_current_user()

  leader.content = request.POST['content']
  leader.put()
  return HttpResponseRedirect('/leaders/view/')


def LeadersDelete(request, key=None):
  if key:
    leader = models.Leader.get(key)
    leader.delete()
  return HttpResponseRedirect('/leaders/view/')


