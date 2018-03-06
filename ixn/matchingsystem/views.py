from django.shortcuts import render, redirect, get_object_or_404
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

def student_form(request, student_code):
    student = get_object_or_404(Student, pk=student_code)
    form = StudentForm(instance = student) # Prepopulate fields
    context = {
        'form': form,
        'student': student
    }
    if(request.method == 'POST'):
        try:
            tag_like_1 = Tag.objects.get(pk=request.POST['tag_like_1'])
            tag_like_2 = Tag.objects.get(pk=request.POST['tag_like_2'])
            tag_like_3 = Tag.objects.get(pk=request.POST['tag_like_3'])
            tag_dislike_1 = Tag.objects.get(pk=request.POST['tag_dislike_1'])
        except(KeyError, Tag.DoesNotExist):
            messages.error(request, 'Tag invalid')
            return render(request, 'matchingsystem/student.html', context)
        else:
            student.tag_like_1 = tag_like_1
            student.tag_like_2 = tag_like_2
            student.tag_like_3 = tag_like_3
            student.tag_dislike_1 = tag_dislike_1
            student.save()
            messages.success(request, 'Form submission successful')
    return render(request, 'matchingsystem/student.html', context)

class StudentList(generic.ListView):
    model = Student
    context_object_name = 'student_list'
    queryset = Student.objects.all()[:10] # Show 10 recent students for now
    template_name = 'matchingsystem/student_list.html'

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
            return redirect('matching')
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
            return redirect('upload')
    else:
        form = UploadForm
    context = {"form": form}
    return render(request, 'admin/upload.html', context)
