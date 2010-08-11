from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from data import Feed

class ExportFeeds(webapp.RequestHandler):
    def get(self,format):
        """ """
        user = users.get_current_user()
        feeds = Feed.all().filter('owner =',user)
        if format == 'csv':
            csv = []
            for feed in feeds:
                csv.append(feed.feed)
            exported = '\n'.join(csv)
        self.response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        self.response.headers.add_header('Content-Disposition','filename=export.%s'%format)
        self.response.out.write(exported)


application = webapp.WSGIApplication(
                                     [
                                         (r'/export/(.*)', ExportFeeds),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


