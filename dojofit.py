#!/usr/bin/env python

# hacker dojo fitness application
#

import cgi
import logging 
import os
import datetime
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template 

import models

"""
application pages
"""
## main page lists active workout sessions
## let's use a template here
class MainPage(webapp2.RequestHandler):
  def get(self):
    sessions = models.ExerciseSession.getAllSessions()
    logging.info( sessions.count() )
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    # self.response.out.write(template.render(path, sessions))
    self.response.out.write(template.render(path, { 'sessions': sessions } ))

## page for displaying the sets of a session
class SetPage(webapp2.RequestHandler):
  def get( self, sid ):
    self.response.out.write('<html><body>')

    sets = models.ExerciseSet.getAllSets()

    for single_set in sets:
      if greeting.user:
        self.response.out.write('<b>%s</b> wrote:' % single_set.user.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s %s</blockquote>' %
                              (single_set.exercisetype, greeting.reps))

    self.response.out.write("""
          <form action="/sign" method="post">
            <div><input name="exercisetype"/></div>
            <div><input name="reps"/></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
        </body>
      </html>""")


"""
data mutation methods via http post
"""
class Guestbook(webapp2.RequestHandler):
  def post(self):
    exerciseset = ExerciseSet()

    if users.get_current_user():
      exerciseset.user = users.get_current_user()

    exerciseset.exercisetype = self.request.get('exercisetype')
    exerciseset.reps = int( self.request.get('reps') )
    exerciseset.put()
    self.redirect('/')


class Session(webapp2.RequestHandler):
  def post(self):
    session = ExerciseSession()
    if users.get_current_user():
      session.user = users.get_current_user()

    session.put()
    self.redirect('/')


"""
application routing and structure
"""
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/session/(.*)', SetPage ),
  ('/sign', Guestbook),
  ('/newsession', Session)
], debug=True)
