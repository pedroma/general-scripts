from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from data import Feed
import feedparser, os

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}

        if user:
            key = self.request.get('remove')
            if key:
                try:
                    Feed.get(key).delete()
                    self.redirect('/')
                except:
                    pass
            if key == 'all':
                feeds = Feed.all().filter('owner =',user)
                for feed in feeds:
                    feed.delete()
                    self.redirect('/')
            logged_in = True
            url = users.create_logout_url(self.request.uri)
            feeds = Feed.all().filter('owner =',user)
            n_feeds = feeds.count()
            if n_feeds != 0:
                feed_url = 'http://%s/feed/%s'%(os.environ['HTTP_HOST'],feeds[0].key())
                template_values.update({'feed_url':feed_url})
            template_values.update({'feeds':feeds,'n_feeds':n_feeds,'nick':user})
        else:
            logged_in = False
            url = users.create_login_url(self.request.uri)

        template_values.update({'logged':logged_in, 'login_url':url})

        self.response.out.write(template.render('index.pt',template_values))

    def post(self):
        user = users.get_current_user()
        feed = self.request.get('feed')
        # check if feed is valid
        lines = feed.split('\n')
        for line in lines:
            f = feedparser.parse(line)
            line = line.replace('\r','')
            if f.get('status',0) in [200,302]:
                feed_obj = Feed(title=f.feed.title,owner=user,feed=line)
                feed_obj.put()
                #template_values = {'logged':True,'error':True}
                #self.response.out.write(template.render('index.pt',template_values))
                #return
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


