import cgi
import datetime
import urllib
import wsgiref.handlers

import models
import utils

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


def guestbookKey(guestbook_name=None):
  """Constructs a datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class Home(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(utils.getTemplate('home'), {}))


class GuestbookView(webapp.RequestHandler):
  def get(self, count):
    guestbook_name=self.request.get('guestbook_name')
    greetings_query = models.Greeting.all().ancestor(
        guestbookKey(guestbook_name)).order('-date')
    greetings = greetings_query.fetch(count)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login to sign guestbook'

    template_values = {
        'greetings': greetings,
        'url': url,
        'url_linktext': url_linktext,
        'user': users.get_current_user(),
    }

    self.response.out.write(template.render(
        utils.getTemplate('guestbook_view'), template_values))


class GuestbookSign(webapp.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = models.Greeting(parent=guestbookKey(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
