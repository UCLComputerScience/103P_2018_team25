"""ixn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from matchingsystem import views

urlpatterns = [
    url(r'^matchingsystem/', include('matchingsystem.urls')),
    url(r'^auth/', include('ixn_auth.urls')),
    url(r'^admin/matchingsystem/matching/$', views.start_matching, name='matching'),
    url(r'^admin/matchingsystem/upload/$', views.upload_data, name='upload'),
    url(r'^admin/', admin.site.urls),
]
