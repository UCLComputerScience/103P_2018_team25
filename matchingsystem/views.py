from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Student, Project, Tag, Module, Project_assignment
from .forms import StudentForm, ProjectForm, MatchingForm, UploadForm
from django.template.response import TemplateResponse
from .tables import ResultTable
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

def index(request):
    return render(request, 'matchingsystem/index.html')

def check_not_student(username):
    try:
        float(username)
        return False
    except ValueError:
        return True

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
            form = StudentForm(request.POST, instance=student)
            if(form.is_valid()): # If all the data has been filled in, validate and save to database
                tag_like_1 = form.cleaned_data.get('tag_like_1')
                tag_like_2 = form.cleaned_data.get('tag_like_2')
                tag_like_3 = form.cleaned_data.get('tag_like_3')
                tag_dislike_1 = form.cleaned_data.get('tag_dislike_1')
                options = [tag_like_1, tag_like_2, tag_like_3, tag_dislike_1]
                if(options_unique(options)):
                    form.save()
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

def client_page(request, username):
    if(request.user.is_authenticated() and request.user.get_username() == username and check_not_student(request.user.username)):
        project_list = Project.objects.all().filter(project_user=request.user) # Pass list of projects created by the user to the view
        context = {
            'project_list': project_list,
            'username': username,
        }
        return render(request, 'matchingsystem/client.html', context)
    else:
        return redirect('matchingsystem:index')

def project_form(request):
    if(request.user.is_authenticated() and check_not_student(request.user.username)):
        if(request.method == 'POST'):
            form = ProjectForm(request.POST)
            if(form.is_valid()):
                project = form.save(commit=False)
                project.project_user = request.user
                project.save()
                messages.success(request, 'Project submission successful')
                return redirect('matchingsystem:project_form')
        else:
            form = ProjectForm
        back_url = reverse('matchingsystem:client', args=[str(request.user.username)])
        context = {
            'form': form,
            'back_url': back_url # To allow the user back to their landing page
        }
        return render(request, 'matchingsystem/project.html', context)
    else:
        return redirect('matchingsystem:index')

# Custom admin views to process student data with the matching algorithm

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def post_list(request):
    table = ResultTable(Project_assignment.objects.all())
    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'admin/result.html', {'table':table})
