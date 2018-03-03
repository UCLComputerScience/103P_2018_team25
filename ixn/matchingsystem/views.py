from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from .models import Student, Project, Tag
from .forms import StudentForm, ProjectForm
from .matching import start_matching_algorithm

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
    if(request.method == 'POST'):
        form = StudentForm(request.POST)
        if(form.is_valid()):
            model_instance = form.save(commit=False)
            # Clean and validate data
            #model_instance.save()
            return redirect('matchingsystem:index')
    else:
        form = StudentForm
    context = {
        'form': form
    }
    return render(request, 'matchingsystem/student.html', context)

def project_form(request): # Do same processing here
    if(request.method == 'POST'):
        form = ProjectForm(request.POST)
        if(form.is_valid()):
            model_instance = form.save(commit=False)
            # Clean and validate data
            #model_instance.save()
            return redirect('matchingsystem:index')
    else:
        form = ProjectForm
    context = {
        'form': form
    }
    return render(request, 'matchingsystem/client.html', context)

def start_matching(request): # This function begins the matching algorithm
    context = {}
#start_matching_algorithm() # may need to run this in the background?
    return render(request, 'matchingsystem/matching.html', context)

def results(request):
    context = {}
    return render(request, 'matchingsystem/results.html', context)
