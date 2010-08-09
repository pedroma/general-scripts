from google.appengine.ext import db

class Feed(db.Model):
    owner = db.UserProperty()
    feed = db.URLProperty(required=True)
