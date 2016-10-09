import os
import re
import jinja2
import webapp2
import hashlib
import hmac
import random
from string import letters

from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

SECRET = '9Ij$p_9n6RtM37x'

def make_secure_val(s):
    return "%s|%s" % (s, hmac.new(SECRET, s).hexdigest())

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

def make_salt(length = 5):
    return ''.join(random.choice(letters) for i in xrange(length))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid)
    
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u
    
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(name = name, pw_hash = pw_hash, email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get('user_id')
        return cookie_val and check_secure_val(cookie_val)
    
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    def get(self):
        # Sort the blog posts in descending order from date created ie. show newest blog entries on top
        blog_posts = BlogPost.all().order('-created')
        username = ''
        if self.user:
            username = self.user.name
        self.render("blog.html", username=username, blog_posts=blog_posts)

class SignUpPage(Handler):
    def get(self):
        self.render("signup.html")
    
    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        confirm_password = self.request.get("confirm_password")        
        email = self.request.get("email")
        
        params = dict(username = username, email = email)
        if not username:
            params['error_username'] = "That's not a valid username"
            have_error = True

        if not password:
            params['error_password'] = "That's not a valid password"
            have_error = True

        if password != confirm_password:
            params['error_confirm_password'] = "Your passwords don't match"
            have_error = True
        
        if have_error:
            self.render("signup.html", **params)
        else:
            u = User.by_name(username)
            if u:
                params['error_username_exists'] = 'That username already exists'
                self.render('signup.html', **params)
            else:
                u = User.register(username, password, email)
                u.put()
                self.login(u)
                self.redirect('/welcome')

class LoginPage(Handler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        params = dict(username = username)
        
        if not username:
            params['error_username'] = "That's not a valid username"
            have_error = True

        if not password:
            params['error_password'] = "That's not a valid password"
            have_error = True
        
        if have_error:
            self.render("login.html", **params)
        else:
            u = User.login(username, password)
            if u:
                self.login(u)
                self.redirect('/')
            else:
                params['error_incorrect_information'] = "Username or password is incorrect"
                self.render("login.html", **params)
            
class PostPage(Handler):
    def get(self):
        pass

class LogoutPage(Handler):
    def get(self):
        self.logout()
        self.render('logout.html')

class WelcomePage(Handler):
    def get(self):
        if self.user:
            self.render("welcome.html", username=self.user.name)
        else:
            self.redirect("/signup")

class NewPostPage(Handler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/signup")

    def post(self):
        if self.user:
            have_error = False
            title = self.request.get("title")
            content = self.request.get("content")
            params = dict(title = title, content = content)
            
            if not title:
                params['error_title'] = "Please enter a title."
                have_error = True
                
            if not content:
                params['error_content'] = "Please enter some content."            
                have_error = True
            
            if have_error:
                self.render('newpost.html', **params)
            else:
                a = BlogPost(title=title, content=content, author=self.user.name)
                a.put()
                params['post_success'] = "Blog entry successfully posted!"
                self.render("newpost.html", **params)
        else:
            self.redirect("/signup")

app = webapp2.WSGIApplication([
    ('/?', MainPage),
    ('/welcome', WelcomePage),
    ('/newpost', NewPostPage),
    ('/([0-9]+)', PostPage),
    ('/logout', LogoutPage),
    ('/signup', SignUpPage),
    ('/login', LoginPage)], debug=True)