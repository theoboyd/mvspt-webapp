from google.appengine.ext import db

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

class Score(db.Model):
  """A score in PD."""
  value = db.IntegerProperty()
  action = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  player = db.UserProperty()
