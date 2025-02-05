# issues/urls.py
from django.urls import path
from . import views  # Import views from the same app or module

urlpatterns = [
    path('', views.index, name='index'),  # Example path
    # Add other paths as needed
]
