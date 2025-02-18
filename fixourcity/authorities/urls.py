# authorities/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.authority_dashboard, name='authority_dashboard'),
    path('assign-contractor/<int:issue_id>/', views.assign_contractor, name='assign_contractor'),
]
