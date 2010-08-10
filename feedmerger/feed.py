from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from data import Feed
import feedparser

class GenerateFeed(webapp.RequestHandler):
    """ """
    def get(self,key):
        template_values = {}
        try:
            feed = Feed.get(key)
            user = feed.owner
        except:
            return "Unauthorized"
        feeds = Feed.all().filter('owner =',user)
        entries = []

        def handle_result(rpc):
            result = rpc.get_result().content
            f = feedparser.parse(result)
            entries.extend(f.entries)

        # Use a helper function to define the scope of the callback.
        def create_callback(rpc):
            return lambda: handle_result(rpc)

        urls = [feed.feed for feed in feeds]
        rpcs = []
        for url in urls:
            rpc = urlfetch.create_rpc()
            rpc.callback = create_callback(rpc)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)

        for rpc in rpcs:
            rpc.wait()

        decorated = [(entry["date_parsed"], entry) for entry in entries]
        decorated.sort()
        decorated.reverse() # for most recent entries first
        sorted = [entry for (date,entry) in decorated]
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


