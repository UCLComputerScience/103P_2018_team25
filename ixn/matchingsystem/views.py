from django.shortcuts import render
from django.http import HttpResponse
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
    return HttpResponse("Student form index")

def client_form(request):
    return HttpResponse("Client form index")

def results(request):
    return HttpResponse("Results page index")
