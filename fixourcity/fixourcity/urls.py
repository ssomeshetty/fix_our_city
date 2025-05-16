
# mycity/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
# urls.py
from public.views import view_notifications, mark_notification_read, mark_all_notifications_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues/', include('issues.urls')),
    path('public/', include('public.urls')),
    path('authorities/', include('authorities.urls')),
    path('contractors/', include('contractor.urls')),
    path('', TemplateView.as_view(template_name='base.html'), name='base'), 
        # ... your existing URLs ...
    path('notifications/', view_notifications, name='view_notifications'),
    path('notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

