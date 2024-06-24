# ---------------------
# Django Imports
# ---------------------
from django.urls import path
from . import views

# ---------------------
# Define url patterns
# ---------------------
# Each path is defined and directed to corresponding view.
# For example, the home path is directed to the home view, which is responsible for rendering the base.html template.

urlpatterns = [
    path("", views.home, name="home"),
]
