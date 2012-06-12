from google.appengine.ext import db

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
    return db.GqlQuery("SELECT * FROM ExerciseSet where id = ?", sid )

## represents the group workout activity at the dojo
class ExerciseSession(db.Model):
  user = db.UserProperty()
  active = db.BooleanProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  @staticmethod
  def getAllSessions():
    return db.GqlQuery("SELECT * FROM ExerciseSession" )

