from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from data import Feed
import feedparser

class GenerateFeed(webapp.RequestHandler):
    """ """
    def get(self):
        template_values = {}
        user = users.get_current_user()
        feeds = Feed.all().filter('owner =',user)
        entries = []
        for feed in feeds:
            f = feedparser.parse(feed.feed)
            entries.extend(f['entries'])
        template_values.update({'entries':entries})
        pt = template.render('feed.pt',template_values)
        self.response.out.write(pt)

application = webapp.WSGIApplication(
                                     [
                                         ('/feed.*', GenerateFeed),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


