# Copyright 2011 Theodore Boyd
import cgi
import datetime
import logging
import re
import urllib

import models
import strategies
import settings
from utils.BeautifulSoup import BeautifulSoup

from google.appengine.ext import db
from google.appengine.api import users

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader

ADMIN_EMAIL = 'theoboyd@gmail.com'
HISTORY_SEPARATOR = ','


def Start(request):
  '''Start AJAX file upload'''
    csrf_token = get_token(request)
    return render_to_response('import.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()


def UserInfo(path):
  '''Returns auth user info'''
  user = ''
  if users.get_current_user():
    login_url = users.create_logout_url(path)
    login_linktext = 'Sign out'
    user = users.get_current_user()
  else:
    login_url = users.create_login_url(path)
    login_linktext = 'Sign in'
  try:
    is_admin = users.get_current_user().email() == ADMIN_EMAIL
  except AttributeError:
    is_admin = False

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
  template_values = {
      'scores_active': True,
  }

  if users.get_current_user():
    player = models.GetOrCreatePlayer(users.get_current_user())
    scores = filter(None, player.score_history.split(HISTORY_SEPARATOR))

    template_values['scores'] = scores
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('scores_view.html', template_values)


def ScoresAdd(request):
  player = models.GetOrCreatePlayer(users.get_current_user())
  my_action = request.POST['action']

  # Computer playes against player:
  opp_action = strategies.play(my_action, player)

  # Score calculator using classical payoff matrix:
  (my_score, opp_score) = strategies.getScore(my_action, opp_action)

  player.score += my_score
  #TODO increment computer score too

  # Generate history stack
  player.score_history = my_action[0] + str(my_score) + opp_action[0] + str(opp_score) + HISTORY_SEPARATOR + player.score_history
  player.put()

  return HttpResponseRedirect('/scores/view/')


def ScoresDelete(request):
  player = models.GetOrCreatePlayer(users.get_current_user())
  player.score_history = ''
  player.put()
  return HttpResponseRedirect('/scores/view/')


def LeadersView(request):
  leaders_query = models.Player.all().order('-score')
  leaders = leaders_query.fetch(100)
  #for l in leaders:
  #  extended_history = filter(None, l.score_history.split(HISTORY_SEPARATOR))
  #  for eh in extended_history:
  #    l.extended_history += eh[0] + ' vs. ' + eh[1] + HISTORY_SEPARATOR
  #  l.extended_history = extended_history
  #TODO better history display
  #TODO leaderboard profile pages
  #TODO special creator profile page

  template_values = {
      'leaders': leaders,
      'leaders_active': True,
      'submit_disabled': True,
  }
  template_values.update(UserInfo(request.get_full_path()))
  return render_to_response('leaders_view.html', template_values)
