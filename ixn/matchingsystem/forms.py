from django.forms import ModelForm, Form, ModelChoiceField, FileField, IntegerField
from .models import Student, Project, Module
from .matching import start_matching_algorithm

MAX_TEAM_SIZE = 5

# Forms for basic data input

class StudentForm(ModelForm): # Use ModelForm docs to format later
    class Meta:
        model = Student
        fields = '__all__' # grab all fields for now

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

# Forms for custom admin views

class MatchingForm(Form):
    module = ModelChoiceField(queryset=Module.objects.all())
    team_size = IntegerField(min_value=1, max_value=MAX_TEAM_SIZE)

    def save(self):
        selected_module = self.cleaned_data['module']
        selected_team_size = self.cleaned_data['team_size']
        start_matching_algorithm(selected_module, selected_team_size)
        

class UploadForm(Form): # TODO add correct fields and save
    student_data = FileField()
    exam_results = FileField()

    def save(self):
        print("upload form")
        student_records = csv.reader(self.cleaned_data['student_data'])
        for line in records:
            pass # Add to tables
        
        student_exams = csv.reader(self.cleaned_data['exam_results'])
        for line in student_exams:
            pass # Add to tables

