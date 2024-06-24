# ---------------------
# Django Imports
# ---------------------

from django.shortcuts import render

# Import generic views from Django
from django.views import generic

# Import Blogpost and Comment models
from .models import Blogpost, Comment

# ---------------------
# Define home function
# ---------------------
# This function renders the base.html page when the home URL is requested.
def home(request):
    return render(request, 'base.html')

# ---------------------
# PostList View
# ---------------------
# This class-based view displays all blogposts that are marked as published (status=1),
# ordered by the date they were created. It uses pagination to display a set number of posts per page.
class PostList(generic.ListView):
    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by('created_on')
    template_name = 'index.html'
    paginate_by = 8
