
# mycity/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues/', include('issues.urls')),
    path('public/', include('public.urls')),
    path('authorities/', include('authorities.urls')),
    path('contractors/', include('contractor.urls')),
    path('', TemplateView.as_view(template_name='base.html'), name='base'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)