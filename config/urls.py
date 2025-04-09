
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views  # Import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.register_view, name='register'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/members/', views.manage_members, name='manage_members'),
    path('admin/news/', views.manage_news, name='manage_news'),
    path('admin/tourism/', views.manage_tourism, name='manage_tourism'),


    path('', include('apps.core.urls')),
    path('members/', include('apps.members.urls')),
    path('news/', include('apps.news.urls')),
    path('tourism/', include('apps.tourism.urls')),
    path('support/', include('apps.support.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
