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
data mutation methods post
"""
class AddUser(webapp2.RequestHandler):
  def post(self):
    sid = self.request.get( 'sid' )
    user = self.request.get( 'user' )
    session = models.ExerciseSession.getSingleSessionData( sid )
    session['users'].append( 
      { 'exercises': {'pushups':[], 'pullups':[]}, 'name': user }
    )
    models.ExerciseSession.setSingleSessionData( sid, session )
    self.redirect('/session/' + sid )

class NewSet(webapp2.RequestHandler):
  def post(self, sid ):
    user = self.request.get( 'user' )
    exercise = self.request.get( 'exercise' )
    reps = self.request.get( 'reps' )
    models.ExerciseSession.addSet( sid, user, exercise, reps ) 
    self.redirect('/session/' + sid )

class NewSession(webapp2.RequestHandler):
  def post(self):
	sessiondata = { 
		'users': [], 
		'exercises': ['pullups','pushups']  
	} 
	session = models.ExerciseSession()
	session.data = pickle.dumps( sessiondata )
	session.put()
	sid = session.key().id()
	self.redirect('/session/' + str(sid) )

class CloseSession(webapp2.RequestHandler):
  def post(self, sid):
    models.ExerciseSession.closeSession( sid )
    self.redirect('/session/' + str(sid) )

"""
application routing and structure
"""
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/session/(.*)', SessionTest ),
  ('/newsession', NewSession),
  ('/closesession/(.*)', CloseSession),
  ('/adduser', AddUser),
  ('/newset/(.*)', NewSet)
], debug=True)

