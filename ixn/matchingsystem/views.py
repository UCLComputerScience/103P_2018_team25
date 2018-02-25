from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Student, Project, Tag

def index(request):
    # Just displays all data from table
    students = Student.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()
    context = {
        'students': students,
        'projects': projects,
        'tags': tags
    }
    return render(request, 'matchingsystem/index.html', context)

def student_form(request):
    context = {}
    return render(request, 'matchingsystem/student.html', context)

def client_form(request):
    context = {}
    return render(request, 'matchingsystem/client.html', context)

def results(request):
    context = {}
    return render(request, 'matchingsystem/results.html', context)
