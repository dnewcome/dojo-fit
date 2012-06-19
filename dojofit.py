#!/usr/bin/env python

'''             
hacker dojo fitness application
'''              

import os
import cgi
import logging 
import datetime
import webapp2
import pickle

from google.appengine.api import users
from google.appengine.ext.webapp import template 

# our application data model
import models

"""
application pages
"""
## main page lists active workout sessions
class MainPage(webapp2.RequestHandler):
  def get(self):
    sessions = models.ExerciseSession.getAllSessions()
    logging.info( sessions.count() )
    path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
    self.response.out.write(template.render(path, {'sessions': sessions}))

class SessionTest(webapp2.RequestHandler):
  def get( self, sid ):

    session = models.ExerciseSession.getSingleSessionData( sid )
    session["sid"] = sid
    session["reprange"] = range(101) 

    path = os.path.join(os.path.dirname(__file__), 'templates/session.html')
    self.response.out.write(template.render(path, session ))

"""
application routing and structure
"""
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/session/(.*)', SessionTest )
], debug=True)

