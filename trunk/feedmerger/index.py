from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from data import Feed
import feedparser

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}

        if user:
            key = self.request.get('remove')
            if key:
                Feed.get(key).delete()
            logged_in = True
            url = users.create_logout_url(self.request.uri)
            feeds = Feed.all().filter('owner =',user)
            template_values.update({'feeds':feeds})
        else:
            logged_in = False
            url = users.create_login_url(self.request.uri)

        template_values.update({'logged':logged_in, 'login_url':url})

        self.response.out.write(template.render('index.pt',template_values))

    def post(self):
        user = users.get_current_user()
        feed = self.request.get('feed')
        # check if feed is valid
        f = feedparser.parse(feed)
        if f.get('status',0) != 200:
            template_values = {'logged':True,'error':True}
            self.response.out.write(template.render('index.pt',template_values))
            return
        feed_obj = Feed(title=f['feed']['title'],owner=user,feed=feed)
        feed_obj.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [
                                         ('/', MainPage),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

