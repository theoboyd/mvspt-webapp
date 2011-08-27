import os

def getTemplate(name):
  return os.path.join(os.path.dirname(__file__), 'templates/%s.html' % name)
