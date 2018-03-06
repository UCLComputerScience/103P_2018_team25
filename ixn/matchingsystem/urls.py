from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'matchingsystem'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student/(?P<student_code>[0-9]+)/$', views.student_form, name='student_form'),
    url(r'^student/', views.StudentList.as_view(), name='student_list'),
    url(r'^client/', views.project_form, name='project_form'),
]
