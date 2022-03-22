"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import app.views


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', app.views.index, name='index'),
    path('', app.views.index_pre_login, name='index_pre_login'),
    path('index', app.views.index, name='index'),
    path('add_tutor', app.views.add_tutor, name='add_tutor'),
    path('add_user', app.views.add_user, name='add_user'),
    path('view/<str:student_id_mod_code>', app.views.view, name='view'),
    path('edit/<str:student_id_mod_code>', app.views.edit, name='edit'),
    path('login', app.views.login, name='login')
]
