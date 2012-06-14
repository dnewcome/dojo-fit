import logging
import pickle

from google.appengine.ext import db

"""
data model for the dojo fitness application.

A session is a collection of sets by various users.

The data model is just a python object that is persisted to the 
Google data store as a blob using pickle. Eventually we might
want a data model that maps better to GQL natively but for
now this works ok.

Example of data for a single session:

session = { 
	'users': [
		{'name': 'dan', 'exercises': {'pushups': [20,10,5], 'pullups': [5, 7]} },
		{'name': 'vikram', 'exercises': {'pushups': [10,10], 'pullups': [5, 7]} },
		{'name': 'marat', 'exercises': {'pushups': [20,30], 'pullups': [5, 7]} }
	], 
	'exercises': ['pullups','pushups']  
} 
 
Note that we store the exercise names redundantly for convenience. We might want
to write some functionality that reduces a set from the rest of the entries.

"""
## represents the group workout activity at the dojo
class ExerciseSession(db.Model):
  user = db.UserProperty()
  active = db.BooleanProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  data = db.TextProperty()

  @staticmethod
  def getSingleSessionData( sid ):
    # must cast explicitly to str here, unpickle fails otw
    return pickle.loads( str(ExerciseSession.getSingleSession( sid ).data) )

  ''' update the data blob for a session '''
  @staticmethod
  def setSingleSessionData( sid, data ):
    session = ExerciseSession.getSingleSession( sid )
    session.data = pickle.dumps( data )
    session.put()

  ''' fetch gql model for a session '''
  @staticmethod
  def getSingleSession( sid ):
    # return db.GqlQuery("SELECT * FROM ExerciseSession" )
	return ExerciseSession.get_by_id( int(sid) )

  ''' fetch list of models for all sessions '''
  @staticmethod
  def getAllSessions():
    return db.GqlQuery("SELECT * FROM ExerciseSession" )

  ''' main way to add a new set to an existing session '''
  @staticmethod
  def addSet( sid, user, exercise, reps ):
    session = ExerciseSession.getSingleSessionData( sid )
    usersets = None
    usersets = find( lambda u: u['name'] == user, session['users'] )
    usersets['exercises'][exercise].append( int(reps) )
    ExerciseSession.setSingleSessionData( sid, session )

''' utility functions '''
def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item

