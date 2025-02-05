
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('public.urls')),  # Include the accounts app URLs
    path('issues/', include('issues.urls')),
    path('', TemplateView.as_view(template_name='base.html'), name='base'), 


]

