from google.appengine.ext import db
from google.appengine.ext.db import polymodel

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

class Player(polymodel.PolyModel):
  """A human or computer player."""
  #PolyModels can be inherited from but their properties cannot be overriden.
  name = db.StringProperty()

class Human(Player):
  """A human player."""
  appengine_user = db.UserProperty()

class Score(db.Model):
  """A score in PD."""
  value = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  player = Player()

class Computer(Player):
  """A computer player."""
  strategy = Strategy()
  scores = db.ListProperty(Score)
