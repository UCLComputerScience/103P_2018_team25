from django.conf.urls import url
from . import views

app_name='ixn_auth'
urlpatterns = [
    url(r'^login', views.ucl_login, name='login'),
    url(r'^logout', views.ucl_logout, name='logout'),
    url(r'^callback', views.ucl_callback_url, name='callback'),
]
