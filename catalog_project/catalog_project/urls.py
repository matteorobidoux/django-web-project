"""catalog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('administration.urls'), name='admin'),
    path('', include('item_catalog.urls'), name='item_catalog'),
    path('messages/', include('messaging.urls'), name='messaging'),
    path('api/', include('item_api.urls'), name='api'),
    path('', include('user_management.urls'), name='user_management'),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'item_catalog.views.response_not_found_404'

