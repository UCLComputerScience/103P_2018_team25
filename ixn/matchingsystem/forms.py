from django import forms
import csv, io
from .models import Student, Project, Module, StudentModule
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

    def get_file_for_read(self, f):
        csv_file = io.StringIO(f.read().decode('utf-8'))
        reader = csv.reader(csv_file, delimiter=',')
        return reader

    def add_students(self, f):
        csv_file = self.get_file_for_read(f)
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
            except Student.DoesNotExist:
                student = Student(student_code=line[STUDENT_CODE_COL], surname=line[STUDENT_SURNAME_COL], forename=line[STUDENT_FORENAME_COL]) # Create the new student
            student.save()

            try:
                student_module = StudentModule.objects.get(student=student, module=module) # If the link exists don't create it again
            except StudentModule.DoesNotExist:
                student_module = StudentModule(student=student, module=module) # Create a new link
            student_module.save()

    def add_exams(self, f):
        csv_file = self.get_file_for_read(f)
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
