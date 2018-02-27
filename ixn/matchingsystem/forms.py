from django.forms import ModelForm, Widget
from .models import Student, Project

#Forms for basic data input

class StudentForm(ModelForm): # Use ModelForm docs to format later
    class Meta:
        model = Student
        fields = '__all__' # grab all fields for now


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
