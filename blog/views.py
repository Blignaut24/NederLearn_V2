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


class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a new blog post. Requires user to be logged in.
    """
    model = Blogpost
    form_class = BlogpostForm
    template_name = 'blogpost_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         "Your blog post has been created successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blogpost_detail',
            kwargs={'slug': self.object.slug}
        )


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    View for updating an existing blog post. Requires user to be logged in.
    """
    model = Blogpost
    form_class = BlogpostForm
    template_name = 'blogpost_update.html'

    def form_valid(self, form):
        # Ensure the current user is set as the author of the post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         "Your blog post has been updated successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blogpost_detail', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        # Only allow editing posts owned by the user
        return Blogpost.objects.filter(author=self.request.user)


class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    View for deleting an existing blog post. Requires user to be logged in.
    """
    model = Blogpost
    template_name = 'blogpost_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request,
                         "Your blog post has been deleted successfully.")
        return response

    success_url = reverse_lazy('my_posts')

    def get_queryset(self):
        # Only allow deleting posts owned by the user
        return Blogpost.objects.filter(author=self.request.user)


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """
    View that lists blog posts created by the logged-in user.
    """
    model = Blogpost
    template_name = 'my_posts.html'
    context_object_name = 'my_blogposts'
    paginate_by = 6

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user)\
            .order_by('-created_on')


class BlogPostList(generic.ListView):
    """
    A view that displays a list of blog posts. It inherits from Django's
    generic ListView. The view filters blog posts by their status and orders
    them by the creation date.Pagination is applied to limit the number of
    posts displayed per page.
    """
    model = Blogpost
    context_object_name = 'blogposts'
    template_name = 'index.html'
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method to check user authentication status.
        This method is called before any other method in the view. It checks if
        the user is authenticated. If the user is not authenticated, they are
        redirected to the login page. Otherwise, the normal flow of the
        ListView is executed.
        """
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter blog posts by media category
        queryset = Blogpost.objects.filter(status=1).order_by('-created_on')
        media_category = self.request.GET.get('category')
        if media_category:
            queryset = queryset.filter(
                media_category__media_name=media_category
                )
        return queryset

    def get_context_data(self, **kwargs):
        # Add media categories to the context for filtering in the template
        context = super().get_context_data(**kwargs)
        context['categories'] = MediaCategory.objects.all()
        return context


class BlogPostDetail(View):
    """
    A view for displaying the detail of a specific blog post, identified by its
    slug. It handles both GET requests to display the post and its comments,
    and POST requests for submitting comments on the post.
    """
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
        """
        Processes the submission of a comment on a blog post. Validates and
        saves the comment, then re-renders the blog post detail page with the
        new comment and a cleared comment form.
        """
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


class LikeUnlike(View):
    """
    A view for handling the liking and unliking of a blog post.
    It updates the like status of a post for the logged-in user.
    """
    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)

        return HttpResponseRedirect(reverse('blogpost_detail', args=[slug]))


# --- PROFILES ---
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """
    A view for displaying the profile of the currently logged-in user.
    It fetches and displays the user's profile data.
    """
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            'profile': user_profile,
            'is_own_profile': True
        }
        return render(request, 'profile.html', context)


class OtherUserProfileView(LoginRequiredMixin, View):
    """
    A view for displaying the profile of another user, specified by their
    username. It retrieves and displays the profile information of the
    specified user.
    """
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            'profile': user_profile,
            'is_own_profile': request.user == user
        }
        return render(request, 'profile.html', context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    A view for editing the profile of the currently logged-in user.
    It handles GET requests to display the profile edit form and POST requests
    to submit the form and update the user's profile.
    """
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
                             "Your profile has been updated successfully.")
            return redirect('profile')

        return render(request, 'profile_edit.html', {'form': form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting the currently logged-in user's account.
    This view ensures that only the logged-in user can delete their own
    account. After successful deletion, the user is logged out and redirected
    to the login page.
    """
    model = User
    template_name = "account_manage.html"
    success_url = reverse_lazy('account_login')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response


def bookmarked(request):
    """
    This view displays the list of blog posts bookmarked by the logged-in user.
    If the user is not authenticated, an empty list is returned.
    It renders the 'bookmarked.html' template with the bookmarked posts.
    """
    if request.user.is_authenticated:
        bookmarked_posts = Blogpost.objects.filter(bookmarks=request.user)
    else:
        bookmarked_posts = []

    return render(request, 'bookmarked.html',
                  {'bookmarked_posts': bookmarked_posts})


class BookmarkUnbookmark(View):
    """
    This view handles the addition or removal of a blog post from the user's
    bookmarked list. It updates the bookmark status upon a POST request and
    redirects to the blog post's detail page with a success message.
    """
    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.bookmarks.filter(id=request.user.id).exists():
            blogpost.bookmarks.remove(request.user)
            messages.success(request, "Removed from 'Bookmarked'.")
        else:
            blogpost.bookmarks.add(request.user)
            messages.success(request, "Added to 'Bookmarked'.")
        return HttpResponseRedirect(reverse('blogpost_detail', args=[slug]))


# --- ERROR HANDLERS ---
def custom_403_error(request, exception):
    """
    Custom error handler for HTTP 403 Forbidden errors. It renders the
    '403.html' template to provide a user-friendly error message.
    """
    return HttpResponseForbidden(render(request, '403.html'))


def custom_405_error(request, exception):
    """
    Custom error handler for HTTP 405 Method Not Allowed errors. It renders
    the '405.html' template to inform users when a HTTP method is not supported
    for the requested URL.
    """
    return HttpResponseNotAllowed(render(request, '405.html'))