from django import forms
from django.contrib import messages
import csv, io
from .models import Student, Project, Module
from .matching import start_matching_algorithm

MAX_TEAM_SIZE = 5

# Forms for data input

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['student_code', 'forename', 'surname', 'email', 'previous_leader', 'exam_results', 'student_modules']
        widgets = {
            'tag_like_1': forms.RadioSelect, # Use radio select widgets
            'tag_like_2': forms.RadioSelect,
            'tag_like_3': forms.RadioSelect,
            'tag_dislike_1': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs): # Prevent null answers
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['tag_like_1'].empty_label = None
        self.fields['tag_like_2'].empty_label = None
        self.fields['tag_like_3'].empty_label = None
        self.fields['tag_dislike_1'].empty_label = None

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['project_tags', 'project_complexity', 'project_module', 'project_valid', 'project_user']

# Forms for custom admin views

def validate_file_extension(f):
    if not f.name.endswith('.csv'):
        raise forms.ValidationError("Only .csv files are accepted")

class MatchingForm(forms.Form):
    module = forms.ModelChoiceField(queryset=Module.objects.all(), label='Select module to match')
    team_size = forms.IntegerField(min_value=1, max_value=MAX_TEAM_SIZE, label='Selected team size')

    def save(self):
        selected_module = self.cleaned_data['module']
        selected_team_size = self.cleaned_data['team_size']
        start_matching_algorithm(selected_module, selected_team_size)
        
class UploadForm(forms.Form):
    student_data = forms.FileField(
            validators=[validate_file_extension],
            label='Upload student data')
    exam_results = forms.FileField(
            validators=[validate_file_extension],
            label='Upload exam results')

    def get_file_for_read(self, f):
        csv_file = io.StringIO(f.read().decode('utf-8'))
        reader = csv.reader(csv_file, delimiter=',')
        return reader

    def add_students(self, f, request):
        csv_file = self.get_file_for_read(f)
        MODULE_CODE_COL = 0 # Column numbers from spreadsheet template
        STUDENT_CODE_COL = 1
        STUDENT_SURNAME_COL = 3
        STUDENT_FORENAME_COL = 4
        STUDENT_EMAIL_COL = 11

        next(csv_file, None) # To skip header row
        for line in csv_file:
            module = Module(module_code=line[MODULE_CODE_COL])
            module.save()

            try:
                student = Student.objects.get(pk=line[STUDENT_CODE_COL])
                student.surname = line[STUDENT_SURNAME_COL]
                student.forename = line[STUDENT_FORENAME_COL] # Update details
                student.email = line[STUDENT_EMAIL_COL]
            except Student.DoesNotExist:
                student = Student(student_code=line[STUDENT_CODE_COL], surname=line[STUDENT_SURNAME_COL], forename=line[STUDENT_FORENAME_COL], email=line[STUDENT_EMAIL_COL]) # Create the new student
            except forms.ValidationError:
                messages.error(request, 'Could not import student:' + line[STUDENT_CODE_COL])
                continue
            student.save()
            student.student_modules.add(module)
        
    def add_exams(self, f, request):
        csv_file = self.get_file_for_read(f)
        STUDENT_CODE_COL = 0 # Column numbers from spreadsheet template
        STUDENT_EXAM_COL = 3

        next(csv_file, None)
        for line in csv_file:
            try:
                student = Student.objects.get(pk=line[STUDENT_CODE_COL])
                student.exam_results = line[STUDENT_EXAM_COL]
                student.save()
            except Student.DoesNotExist:
                messages.error(request, 'Invalid student to import exam score: ' + line[STUDENT_CODE_COL])
            except forms.ValidationError:
                messages.error(request, 'Invalid exam score for: ' + line[STUDENT_CODE_COL])
