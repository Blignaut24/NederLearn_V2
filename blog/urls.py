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
                         "Your blog post has been created successfully.")
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
                         "Your blog post has been updated successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blogpost_detail', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        # Only allow editing posts owned by the user
        return Blogpost.objects.filter(author=self.request.user)
