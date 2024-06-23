from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

current_year = timezone.now().year

# ---------------------
# Define Year Validator
# ---------------------
def validate_year(value):
    """
    A check is made to ensure the 'release year' is between 1800 and
    the current year. If the year doesn't fit within this range, an
    error message will appear.
    """
    current_year = timezone.now().year
    if not (1800 <= value <= current_year):
        raise ValidationError(
            _("Please enter a year between 1800 and %(current_year)s"),
            params={'current_year': current_year},
        )

# ---------------------
# Define Your Models
# ---------------------
STATUS = ((0, 'Draft'), (1, 'Published'))

# MediaCategory Model
class MediaCategory(models.Model):
    """
    The MediaCategory model organizes learning materials into 12 unique
    classifications, including movies, series, books, music, podcasts,
    and European Language levels A1 - C2. Each category is used to
    categorize blog posts within the NederLearn app.
    The 'media_name' field is unique, ensuring no category is replicated.
    """
    media_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.media_name

    class Meta:
        verbose_name_plural = "Media Categories"

# Blogpost Model
class Blogpost(models.Model):
    """
    The Blogpost model in the NederLearn application captures details like
    title, author, creation and update times, and content. It also indicates
    the post's status (draft or published), includes an image, media category,
    and year of release, and features 'like' and 'bookmark' options for user
    engagement and reference.
    """
    blog_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=20000)
    excerpt = models.TextField(max_length=500, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField('image', default='placeholder')
    media_category = models.ForeignKey(
        'MediaCategory', on_delete=models.SET_NULL,
        related_name='blog_posts', null=True, blank=True
    )
    #release_year = models.IntegerField(validators=[validate_year], blank=True)
    release_year = models.IntegerField(validators=[validate_year])
    media_link = models.URLField()
    likes = models.ManyToManyField(
        User, related_name='blogpost_likes', blank=True
    )
    bookmarks = models.ManyToManyField(
        User, related_name='blogpost_bookmarks', blank=True
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.blog_title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_bookmarks(self):
        return self.bookmarks.count()

# UserProfile Model
class UserProfile(models.Model):
    """
    The UserProfile model is used to collect additional information
    about the user that isn't included in the basic User model.
    By having a separate UserProfile model, we can keep the User model
    (which handles authentication) simpler and more focused, while still
    being able to store and retrieve more detailed information about our users.
    This information, such as profile picture, location, first language, and
    learning goals, can help in personalizing the user's experience and can
    provide valuable context for certain functionalities in the app.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='placeholder')
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    top_movies = models.CharField(max_length=255, blank=True)
    top_series = models.CharField(max_length=255, blank=True)
    top_music_albums = models.CharField(max_length=255, blank=True)
    top_books = models.CharField(max_length=255, blank=True)
    top_podcasts = models.CharField(max_length=255, blank=True)
    top_miscellaneous = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

# Comment Model
class Comment(models.Model):
    """
The "Comment" model is linked to a particular blog post and its author,
symbolizing a comment made on that post. It stores:

- The content of the comment
- The date and time it was created
- A boolean flag that shows whether site administrators have approved it
    """
    body = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    post = models.ForeignKey('Blogpost', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} by {self.user.username}"