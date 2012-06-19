import webapp2
import models
import pickle

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

prefix = '/service'
service = webapp2.WSGIApplication([
  (prefix + '/newsession', NewSession),
  (prefix + '/closesession/(.*)', CloseSession),
  (prefix + '/adduser', AddUser),
  (prefix + '/newset/(.*)', NewSet)
], debug=True)
