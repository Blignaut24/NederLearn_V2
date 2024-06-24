# jshint esversion: 6

# ---------------------
# Django Imports
# ---------------------

from django.shortcuts import render

# Import generic views from Django
from django.views import generic

# Import Blogpost model
from .models import Blogpost

# ---------------------
# BlogPostList View
# ---------------------
# This class-based view displays a list of published blogposts, sorted by creation date. The list is paginated.
class BlogPostList(generic.ListView):
    model = Blogpost
    context_object_name = 'blogposts'
    template_name = 'index.html'
    paginate_by = 6

    # ---------------------
    # Dispatch Method
    # ---------------------
    # This method is called before any other method in the view. It checks if
    # the user is authenticated. If not, they are redirected to the login page.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    # ---------------------
    # Get Queryset Method
    # ---------------------
    # This method filters blogposts by media category and orders them by creation date.
    def get_queryset(self):
        queryset = Blogpost.objects.filter(status=1).order_by('-created_on')
        media_category = self.request.GET.get('category')
        if media_category:
            queryset = queryset.filter(
                media_category__media_name=media_category
                )
        return queryset

    # ---------------------
    # Get Context Data Method
    # ---------------------
    # This method adds media categories to the context for filtering in the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MediaCategory.objects.all()
        return context
