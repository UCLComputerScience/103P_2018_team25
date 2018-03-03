from django import forms
import csv
from .models import Student, Project, Module
from .matching import start_matching_algorithm

MAX_TEAM_SIZE = 5

# Forms for basic data input

class StudentForm(forms.ModelForm): # Use ModelForm docs to format later
    class Meta:
        model = Student
        fields = '__all__' # grab all fields for now

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

# Forms for custom admin views

def validate_file_extension(f):
    if not f.name.endswith('.csv'):
        raise forms.ValidationError("Only .csv files are accepted")

class MatchingForm(forms.Form):
    module = forms.ModelChoiceField(queryset=Module.objects.all())
    team_size = forms.IntegerField(min_value=1, max_value=MAX_TEAM_SIZE)

    def save(self):
        selected_module = self.cleaned_data['module']
        selected_team_size = self.cleaned_data['team_size']
        start_matching_algorithm(selected_module, selected_team_size)
        
class UploadForm(forms.Form):
    student_data = forms.FileField(validators=[validate_file_extension])
    exam_results = forms.FileField(validators=[validate_file_extension])

    def save(self):
        student_records = csv.reader(self.cleaned_data['student_data'])
        for line in student_records:
            pass # Add to tables
        
        student_exams = csv.reader(self.cleaned_data['exam_results'])
        for line in student_exams:
            pass # Add to tables
