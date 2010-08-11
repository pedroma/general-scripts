from google.appengine.ext import db

class Feed(db.Model):
    title = db.StringProperty()
    owner = db.UserProperty()
    feed = db.URLProperty(required=True)
    limit = db.IntegerProperty(default = 10)
