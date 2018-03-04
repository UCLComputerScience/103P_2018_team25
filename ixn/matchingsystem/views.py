from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
import csv, io
from .models import Student, Project, Tag, Module, StudentModule
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
            # Clean and validate data
            #model_instance.save()
            return redirect('matchingsystem:index')
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
            # Clean and validate data
            #model_instance.save()
            return redirect('matchingsystem:index')
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
            return redirect('admin:index')
    else:
        form = MatchingForm
    context = {"form": form}
    return render(request, 'matchingsystem/matching.html', context)

def upload_data(request):
    if(request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if(form.is_valid()):
            student_records = request.FILES['student_data'].read().decode('utf-8')
            student_records = io.StringIO(student_records)
            student_records = csv.reader(student_records, delimiter=',')
            add_students(student_records)

            student_exams = request.FILES['exam_results'].read().decode('utf-8')
            student_exams = io.StringIO(student_exams)
            student_exams = csv.reader(student_exams, delimiter=',')
            add_exams(student_exams)
            return redirect('admin:index') # TODO Redirect to a success page
    else:
        form = UploadForm
    context = {"form": form}
    return render(request, 'matchingsystem/upload.html', context)

def add_students(csv_file):
    MODULE_CODE_COL = 0 # Column numbers from spreadsheet template
    STUDENT_CODE_COL = 1
    STUDENT_SURNAME_COL = 3
    STUDENT_FORENAME_COL = 4

    next(csv_file, None) # To skip header row
    for line in csv_file:
        module = Module(module_code=line[MODULE_CODE_COL])
        module.save()

        try:
            student = Student.objects.get(pk=line[STUDENT_CODE_COL])
            student.surname = line[STUDENT_SURNAME_COL]
            student.forename = line[STUDENT_FORENAME_COL] # Update details
        except Exception:
            student = Student(student_code=line[STUDENT_CODE_COL], surname=line[STUDENT_SURNAME_COL], forename=line[STUDENT_FORENAME_COL]) # Create the new student
        student.save()

        try:
            student_module = StudentModule.objects.get(student=student, module=module) # If the link exists don't create it again
        except Exception:
            student_module = StudentModule(student=student, module=module) # Create a new link
        student_module.save()

def add_exams(csv_file): # TODO Move these to forms, see if can be part of POST
    STUDENT_CODE_COL = 0 # Column numbers from spreadsheet template
    STUDENT_EXAM_COL = 3

    next(csv_file, None) # To skip header row
    for line in csv_file:
        try:
            student = Student.objects.get(pk=line[STUDENT_CODE_COL])
            student.exam_results = line[STUDENT_EXAM_COL]
            student.save()
        except Exception:
            pass # if no student, don't do anything
