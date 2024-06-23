# ---------------------
# Django Imports
# ---------------------
from django.apps import AppConfig

# ---------------------
# BlogConfig Class
# ---------------------
# This class is used to configure the 'blog' application.
class BlogConfig(AppConfig):
    # Define the default auto field
    default_auto_field = 'django.db.models.BigAutoField'

    # Define the application name
    name = 'blog'
