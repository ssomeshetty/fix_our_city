# issues/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_issue, name='create_issue'),
    path('view/', views.view_issues, name='view_issues'),
    path('detail/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('upload-image/<int:issue_id>/', views.upload_issue_image, name='upload_issue_image'),
    path('upvote/<int:issue_id>/', views.upvote_issue, name='upvote_issue'),
    path('issues/<int:issue_id>/rate/', views.rate_contractor, name='rate_contractor'),
    path('issues/<int:issue_id>/add_comment/', views.add_comment, name='add_comment'),


    
]