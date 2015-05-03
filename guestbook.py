import cgi
import urllib

import webapp2

from google.appengine.ext import ndb


class Greeting(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  content = ndb.StringProperty()
  pref = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    self.response.out.write('<h1>survey result:</h1>')
    guestbook_name = self.request.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(20)

    for greeting in greetings:
      self.response.out.write("<blockquote>%s " %
                              cgi.escape(greeting.content))
      self.response.out.write("</blockquote>")

    self.response.out.write("""
        </body>
      </html>""")

class SubmitForm(webapp2.RequestHandler):
  def get(self):
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        pref = self.request.get('pref'), 
                        content = self.request.get('content'))
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', SubmitForm)
])
