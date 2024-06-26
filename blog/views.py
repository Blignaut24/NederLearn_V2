# ---------------------
# Django Imports
# ---------------------
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import Blogpost
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# ---------------------
# Define the home view
# ---------------------
# This function renders a template called 'index.html' when a request is made to the home page.
def home(request):
    return render(request, 'index.html')

# ---------------------
# BlogPostList View
# ---------------------
# This class-based view displays a list of published blogposts, sorted by creation date. The list is paginated.
class BlogPostList(generic.ListView):
    model = Blogpost
    context_object_name = 'blogposts'
    template_name = 'index.html'
    paginate_by = 8

    # ---------------------
    # Dispatch Method
    # ---------------------
    # This method is called before any other method in the view. It checks if the user is authenticated. If not, they are redirected to the login page.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

class LikeUnlike(View):
    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)

        return HttpResponseRedirect(reverse('blogpost_detail', args=[slug]))

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

    paginate_by = 8

# ---------------------
# BlogPostDetail Class
# ---------------------
class BlogPostDetail(View):

    # ---------------------
    # Get Method
    # ---------------------
    def get(self, request, slug, *args, **kwargs):
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = False
        if blogpost.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "liked": liked
            },
        )
