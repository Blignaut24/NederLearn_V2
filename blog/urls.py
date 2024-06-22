# ---------------------
# Importing Libraries
# ---------------------
# Standard library imports
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator

# Third-party imports
from django.views import generic, View
from django.views.generic import DeleteView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Local application/library specific imports
from .models import Blogpost, UserProfile, MediaCategory
from .forms import CommentForm, UserProfileForm, BlogpostForm

# ---------------------
# Defining Views
# ---------------------
# Each view is defined and specific methods are assigned for handling GET and POST requests.
class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blogpost
    form_class = BlogpostForm
    template_name = 'blogpost_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
        "Woohoo! Your blog post just made its grand entrance to the world! Go celebrate!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blogpost_detail',
            kwargs={'slug': self.object.slug}
        )

class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blogpost
    form_class = BlogpostForm
    template_name = 'blogpost_update.html'

    def form_valid(self, form):
        # Ensure the current user is set as the author of the post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
        "Your blog post just got a fabulously fresh facelift!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blogpost_detail', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        # Only allow editing posts owned by the user
        return Blogpost.objects.filter(author=self.request.user)

    

# ---------------------
# BlogpostDeleteView Class
# ---------------------
# This class-based view allows for the deletion of blogposts.
# Only posts owned by the user can be deleted.
class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blogpost
    template_name = 'blogpost_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request,
        "Your blog post just took a one-way trip to the digital trash can!")
        return response

    success_url = reverse_lazy('my_posts')

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user)

# ---------------------
# MyBlogPostsView Class
# ---------------------
# This class-based view lists all blogposts from a user, ordered by creation date.
class MyBlogPostsView(LoginRequiredMixin, ListView):
    model = Blogpost
    template_name = 'my_posts.html'
    context_object_name = 'my_blogposts'
    paginate_by = 6

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user)\
            .order_by('-created_on')

# ---------------------
# BlogPostList Class
# ---------------------
# This class-based view lists all blogposts, ordered by creation date.
# Only blogposts with status=1 (published) are shown.
# Pagination is set to display 8 posts per page.
class BlogPostList(generic.ListView):
    model = Blogpost
    context_object_name = 'blogposts'
    template_name = 'index.html'
    paginate_by = 8

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Blogpost.objects.filter(status=1).order_by('-created_on')
        media_category = self.request.GET.get('category')
        if media_category:
            queryset = queryset.filter(
                media_category__media_name=media_category
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MediaCategory.objects.all()
        return context

# ---------------------
# BlogPostDetail Class
# ---------------------
# This class-based view displays the details of a single blogpost specified by its slug.
class BlogPostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False)\
            .order_by("created_on")
        liked = False
        if blogpost.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False)\
            .order_by("created_on")
        liked = blogpost.likes.filter(id=request.user.id).exists()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": comment_form.is_valid(),
                "liked": liked,
                "comment_form": comment_form
            },
        )

# ---------------------
# LikeUnlike Class
# ---------------------
# This class-based view allows the user to like or unlike a blogpost.
class LikeUnlike(View):
    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)

        return HttpResponseRedirect(reverse('blogpost_detail', args=[slug]))

# Profile Views
# ---------------------
# Import necessary modules and decorators
from django.shortcuts import render
from django.views import generic, View
from .models import Blogpost, Comment, MediaCategory

# ---------------------
# ProfileView: Display user's own profile
# ---------------------
@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            'profile': user_profile,
            'is_own_profile': True
        }
        return render(request, 'profile.html', context)

# ---------------------
# OtherUserProfileView: Display other users' profiles
# ---------------------
class OtherUserProfileView(LoginRequiredMixin, View):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            'profile': user_profile,
            'is_own_profile': request.user == user
        }
        return render(request, 'profile.html', context)

# ---------------------
# ProfileEditView: Allow users to edit their profile
# ---------------------
class ProfileEditView(LoginRequiredMixin, View):

    def get(self, request):
        # Ensure that a UserProfile exists for the user
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, 'profile_edit.html', {'form': form})

    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(request.POST, request.FILES,
                            instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request,
                "Your profile just got a super-duper, ultra-mega, fantabulous makeover! Cue the applause!")
            return redirect('profile')

        return render(request, 'profile_edit.html', {'form': form})

# ---------------------
# ProfileDeleteView: Allow users to delete their account
# ---------------------
class ProfileDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    template_name = "account_manage.html"
    success_url = reverse_lazy('account_login')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response

# ---------------------
# bookmarked: Display bookmarked blog posts for the user
# ---------------------
def bookmarked(request):

    if request.user.is_authenticated:
        bookmarked_posts = Blogpost.objects.filter(bookmarks=request.user)
    else:
        bookmarked_posts = []

    return render(request, 'bookmarked.html',
                {'bookmarked_posts': bookmarked_posts})

# ---------------------
# BookmarkUnbookmark: Allow users to bookmark or remove bookmarks from blog posts
# ---------------------
class BookmarkUnbookmark(View):

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.bookmarks.filter(id=request.user.id).exists():
            blogpost.bookmarks.remove(request.user)
            messages.success(request, "Removed from 'Bookmarked'.")
        else:
            blogpost.bookmarks.add(request.user)
            messages.success(request, "Added to 'Bookmarked'.")
        return HttpResponseRedirect(reverse('blogpost_detail', args=[slug]))

# ---------------------
# Custom Error Handlers
# ---------------------
def custom_403_error(request, exception):
    return HttpResponseForbidden(render(request, '403.html'))

def custom_405_error(request, exception):
    return HttpResponseNotAllowed(render(request, '405.html'))


