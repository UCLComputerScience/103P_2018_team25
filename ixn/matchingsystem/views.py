from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Project, Tag, Module
from .forms import StudentForm, ProjectForm, MatchingForm, UploadForm

def index(request):
    return render(request, 'matchingsystem/index.html')

def student_form(request, student_code):
    # Only allow a student to edit their form
    if(request.user.is_authenticated() and request.user.get_username() == student_code):
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
                options = [tag_like_1, tag_like_2, tag_like_3, tag_dislike_1]
            except(KeyError, Tag.DoesNotExist):
                messages.error(request, 'Invalid tag chosen!')
                return render(request, 'matchingsystem/student.html', context)
            else:
                if(options_unique(options)):
                    student.tag_like_1 = tag_like_1
                    student.tag_like_2 = tag_like_2
                    student.tag_like_3 = tag_like_3
                    student.tag_dislike_1 = tag_dislike_1
                    student.save()
                    messages.success(request, 'Interest submission successful')
                    return redirect('matchingsystem:student_form', student_code)
                else:
                    messages.error(request, 'You cannot select a tag twice!')
        return render(request, 'matchingsystem/student.html', context)
    else:
        return redirect('matchingsystem:index')

def options_unique(options):
    if(len(options) == len(set(options))):
        return True
    return False

class StudentList(generic.ListView): # Remove when permissions are verified
    model = Student
    context_object_name = 'student_list'
    queryset = Student.objects.all()[:10] # Show 10 recent students for now
    template_name = 'matchingsystem/student_list.html'

def project_form(request):
    if(request.method == 'POST'):
        form = ProjectForm(request.POST)
        if(form.is_valid()):
            model_instance = form.save(commit=False)
            model_instance.save()
            messages.success(request, 'Project submission successful')
            return redirect('matchingsystem:project_form')
    else:
        form = ProjectForm
    context = {'form': form}
    return render(request, 'matchingsystem/client.html', context)

def start_matching(request):
    if(request.method == 'POST'):
        form = MatchingForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, 'Matching completed successfully')
            return redirect('matching')
    else:
        form = MatchingForm
    context = {"form": form}
    return render(request, 'admin/matching.html', context)

def upload_data(request):
    if(request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if(form.is_valid()):
            form.add_students(request.FILES['student_data'], request)
            form.add_exams(request.FILES['exam_results'], request)

            messages.success(request, 'Upload successful')
            return redirect('upload')
    else:
        form = UploadForm
    context = {"form": form}
    return render(request, 'admin/upload.html', context)
