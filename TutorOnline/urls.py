"""TutorOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from rooms.views import show_chat_page
from django.conf import settings 
# import notifications.urls
from django.conf.urls.static import static 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('users.urls')),
    path('rooms/',include('rooms.urls')),
    path('',include('core.urls')),
    path('courses/',include('courses.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),

    # path('<str:room_name>/<str:person_name>/', show_chat_page, name='showchat'),

]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

