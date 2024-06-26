# ---------------------
# Django Imports
# ---------------------
from django.urls import path
from . import views
from django.views.generic.base import TemplateView

# ---------------------
# Define url patterns
# ---------------------
# Each path is defined and directed to corresponding view.
# For example, the home path is directed to the home view, which is responsible for rendering the base.html template.

urlpatterns = [
    path("", views.BlogPostList.as_view(), name="home"),
    path('about-us/', TemplateView.as_view(template_name='about_us.html'),
        name='about_us'),
]
