from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from .models import Student, Project, Tag, Module
from .forms import StudentForm, ProjectForm, MatchingForm, UploadForm

def index(request):
    # Just displays all data from table
    students = Student.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()
    modules = Module.objects.all()
    context = {
        'students': students,
        'projects': projects,
        'tags': tags,
        'modules': modules
    }
    return render(request, 'matchingsystem/index.html', context)

def student_form(request):
    if(request.method == 'POST'):
        form = StudentForm(request.POST)
        if(form.is_valid()):
            model_instance = form.save(commit=False)
            #model_instance.save()
            messages.success(request, 'Form submission successful')
            return redirect('matchingsystem:student_form')
    else:
        form = StudentForm
    context = {
        'form': form
    }
    return render(request, 'matchingsystem/student.html', context)

def project_form(request):
    if(request.method == 'POST'):
        form = ProjectForm(request.POST)
        if(form.is_valid()):
            model_instance = form.save(commit=False)
            #model_instance.save()
            messages.success(request, 'Form submission successful')
            return redirect('matchingsystem:project_form')
    else:
        form = ProjectForm
    context = {
        'form': form
    }
    return render(request, 'matchingsystem/client.html', context)

def start_matching(request):
    if(request.method == 'POST'):
        form = MatchingForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, 'Matching successful')
            return redirect('matchingsystem:matching')
    else:
        form = MatchingForm
    context = {"form": form}
    return render(request, 'admin/matching.html', context)

def upload_data(request):
    if(request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if(form.is_valid()):
            form.add_students(request.FILES['student_data'])
            form.add_exams(request.FILES['exam_results'])

            messages.success(request, 'Upload successful')
            return redirect('matchingsystem:upload')
    else:
        form = UploadForm
    context = {"form": form}
    return render(request, 'admin/upload.html', context)
