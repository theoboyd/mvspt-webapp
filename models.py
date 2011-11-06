from google.appengine.ext import db
from google.appengine.api import users


class Comment(db.Model):
  """An individual comment entry with an author, content, and date."""
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class Posting(db.Model):
  """An individual posting."""
  author = db.UserProperty()
  title = db.StringProperty()
  img_url = db.StringProperty()
  post_url = db.StringProperty()
  rating = db.IntegerProperty()
  description = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class Strategy(db.Model):
  """A PD strategy."""


class Player(db.Model):
  """A player with a score history."""
  score = db.IntegerProperty()
  user = db.UserProperty()
  score_history = db.StringProperty()


def GetOrCreatePlayer(current_user):
  player = None
  if current_user:
    players = Player.all().filter('user = ', current_user).fetch(1)
    if players:
      player = players[0]
  if not player:
    player = Player(score=0, user=current_user, score_history='')
    player.put()
  return player
