from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditPost(BlogHandler):

    """ Handler for editing post page

    GET: Get the current post from the path and check if the user has proper
    permissions to edit it.
    POST: Do form validation and then check if the author has permission.
    If so, update the post and then redirect with a message. Else, redirect
    with an error

    """

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            error = ''
            if not post:
                self.error(404)
                return

            if post.author.name != self.user.name:
                return self.redirect(
                    "/blog/%s?error=You don't have access to edit this post."
                    % post_id)

            self.render("editpost.html", subject=post.subject,
                        content=post.content, error=error, post_id=post_id,
                        post=post)
        else:
            return self.redirect("/login")

    def post(self, post_id):
        if self.user:
            subject = self.request.get('subject')
            content = self.request.get('content')
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if subject and content:
                if post.author.name == self.user.name:
                    post.subject = subject
                    post.content = content
                    post.put()
                    return self.redirect(
                        "/blog/%s?message=Post updated successfully!"
                        % post_id)
                else:
                    return self.redirect(
                        "/blog/%s?error=You don't have permission to edit " +
                        "this post!" % post_id)
            else:
                error = "Please enter the subject and content."
                self.render("editpost.html", subject=subject,
                            content=content, error=error, post_id=post_id,
                            post=post)
        else:
            return self.redirect('/login')
