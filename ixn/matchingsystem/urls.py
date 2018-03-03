from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'matchingsystem'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student', views.student_form, name='student_form'),
    url(r'^client', views.project_form, name='project_form'),
    url(r'^results', views.results, name='results'),
    url(r'^matching/$', views.start_matching, name='matching'),
    url(r'^upload/$', views.upload_data, name='upload'),
]
