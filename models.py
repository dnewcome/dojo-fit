import logging
import pickle
from google.appengine.ext import db

def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item

"""
data model for the fitness application.
Sets/Sessions

A session is a collection of sets by various users.
Each set is just a count of number of an exercise performed
"""
class ExerciseSet(db.Model):
  user = db.UserProperty()
  reps = db.IntegerProperty()
  # TODO: should type be an enum or something?
  exercisetype = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  @staticmethod
  def getAllSets():
    return db.GqlQuery("SELECT * FROM ExerciseSet" )

  @staticmethod
  def getSetsForId( sid ):
    return db.GqlQuery("SELECT * FROM ExerciseSet where session = :1", sid )

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

  @staticmethod
  def setSingleSessionData( sid, data ):
    session = ExerciseSession.getSingleSession( sid )
    session.data = pickle.dumps( data )
    session.put()

  @staticmethod
  def getSingleSession( sid ):
    # return db.GqlQuery("SELECT * FROM ExerciseSession" )
	return ExerciseSession.get_by_id( int(sid) )

  @staticmethod
  def getAllSessions():
    return db.GqlQuery("SELECT * FROM ExerciseSession" )

  @staticmethod
  def addSet( sid, user, exercise, reps ):
    session = ExerciseSession.getSingleSessionData( sid )
    # usersets = find( lambda user: user['name'] == user, session['users'])
    usersets = None
    for u in session['users']:
      if u['name'] == user:
        usersets = u
    usersets['exercises'][exercise].append( int(reps) )
    ExerciseSession.setSingleSessionData( sid, session )

  @staticmethod
  def addUserToSession( user, session ):
    usersession = User_Session()
    usersession.user = user
    usersession.session = session 


class User_Session(db.Model):
  user = db.UserProperty()
  session = db.ReferenceProperty(ExerciseSession)
