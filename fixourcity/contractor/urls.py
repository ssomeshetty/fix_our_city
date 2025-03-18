# contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.contractor_dashboard, name='contractor_dashboard'),
    path('update-issue/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),
    path('leaderboard/', views.contractor_leaderboard, name='contractor_leaderboard'),
    path('detail/<int:contractor_id>/', views.contractor_detail, name='contractor_detail'),
    
    
]