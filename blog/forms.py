# Import required modules and models
import datetime
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, UserProfile, Blogpost


# ---------------------
# Blogpost Form
# ---------------------
# This form is used to create or edit a blog post.
class BlogpostForm(forms.ModelForm):

    class Meta:
        model = Blogpost
        fields = [
            'blog_title', 'content', 'excerpt',
            'featured_image', 'media_category',
            'release_year', 'media_link'
        ]

        # Define form widgets and their attributes
        widgets = {
            # Rest of the widgets here...
        }

        # Define form labels
        labels = {
            # Rest of the labels here...
        }

    def __init__(self, *args, **kwargs):
        super(BlogpostForm, self).__init__(*args, **kwargs)
        self.fields['media_link'].initial = '<http://www>.'

    def clean(self):
        cleaned_data = super().clean()
        featured_image = cleaned_data.get('featured_image')

        if not featured_image:
            cleaned_data['featured_image'] = 'blogpost_placeholder'
        return cleaned_data

# ---------------------
# Comment Form
# ---------------------
# This form is used to submit a comment on a blog post.
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

        # Define form widgets and their attributes
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'cols': 50,
                    'placeholder': 'Write your comment here...',
                    'maxlength': '1000'
                }
            ),
        }
        labels = {'body': ''}

# ---------------------
# User Profile Form
# ---------------------
# This form is used to create or edit a user profile.
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'bio', 'country', 'top_movies',
            'top_series', 'top_music_albums', 'top_books',
            'top_podcasts', 'top_miscellaneous'
        ]

        # Define form labels
        labels = {'profile_image': 'Upload Profile Image'}

        # Define form widgets and their attributes
        widgets = {
            # Rest of the widgets here...
        }
