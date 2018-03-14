from django.conf.urls import url
from . import views

app_name='ixn_auth'
urlpatterns = [
    url(r'^student/login', views.ucl_login, name='student_login'),
    url(r'^student/callback', views.ucl_callback_url, name='student_callback'),
    url(r'^client/login', views.client_login, name='client_login'),
    url(r'^client/signup', views.client_signup, name='client_signup'),
    url(r'^logout', views.ucl_logout, name='logout'),
]
