# contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.contractor_dashboard, name='contractor_dashboard'),
    path('update-issue/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),
]