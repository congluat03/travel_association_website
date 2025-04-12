
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as viewsCore
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', viewsCore.custom_login, name='login'),
    path('register/', viewsCore.register_view, name='register'),
    path('admin/', viewsCore.admin_dashboard, name='admin_dashboard'),

    path('admin/members/', include(('apps.members.urls', 'members'), namespace='admin_members')),
    path('admin/news/', include(('apps.news.urls', 'news'), namespace='admin_news')),
    path('admin/support/', include(('apps.support.urls', 'support'), namespace='admin_support')),
    path('admin/tourism/', include('apps.tourism.urls', namespace='tourism')),
    
    path('admin/tourism/', viewsCore.manage_tourism, name='manage_tourism'),
    path('admin/members/add_members', viewsCore.manage_members, name='add_members'),

    path('', include('apps.core.urls')),
    path('members/', include('apps.members.urls')),
    path('news/', include('apps.news.urls')),
    path('tourism/', include('apps.tourism.urls')),
    path('support/', include('apps.support.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
