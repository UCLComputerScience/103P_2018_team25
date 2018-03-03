from django.forms import ModelForm, Form, ModelChoiceField, FileField
from .models import Student, Project, Module

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

class MatchingForm(Form): # TODO add correct fields and save
    module = ModelChoiceField(queryset=Module.objects.all())

    def save(self):
        print("matching form")

class UploadForm(Form): # TODO add correct fields and save
    student_data = FileField()

    def save(self):
        print("upload form")
