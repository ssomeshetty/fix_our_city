

from django.urls import path
from . import views
from public import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name= 'base'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('users/', views.users, name='users'),
    path('contractor/', views.contractor, name='contractor'),
    path('authority/', views.authority, name='authority'),
    # path('register/', user_views.register, name="register"),
    # path('profile/', user_views.profile, name="profile"),
    # path('profile/profile_update/', user_views.profile_update, name="profile-update"),

]