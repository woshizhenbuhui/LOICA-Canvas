"""djangoProject2 URL Configuration

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
from django.urls import path
from django.urls import path
from pywebio.platform.django import webio_view
# import app01.task_func
from django.urls import path
from app01 import views
from django.conf.urls.static import static
from django.conf import settings

# `task_func` is PyWebIO task function
# from app01 import task_func
from app01.views import task_func, task_func2

webio_view_func = webio_view(task_func)
webio_view_func2 = webio_view(task_func2)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('tool/', webio_view_func),
    path('index/', views.index),
    path('showdata/', webio_view_func2),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
