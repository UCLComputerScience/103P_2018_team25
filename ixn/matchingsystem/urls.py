from django.conf.urls import url
from . import views

app_name = 'matchingsystem'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student', views.student_form, name='student_form'),
    url(r'^client', views.client_form, name='client_form'),
    url(r'^results', views.results, name='results'),
]
