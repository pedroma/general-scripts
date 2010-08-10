from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from data import Feed
import feedparser

class GenerateFeed(webapp.RequestHandler):
    """ """
    def get(self,key):
        template_values = {}
        try:
            feed = Feed.get(key)
        except:
            return "Unauthorized"
        user = feed.owner
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
                                         (r'/feed/(.*)', GenerateFeed),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


