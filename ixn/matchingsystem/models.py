from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# These are the models to define database structure (tables, relationships)
# TODO lengths of char fields

MAX_TEAM_LEADER = 3
MAX_PROJECT_COMPLEXITY = 5

def get_integer_choices(start, finish): 
    # Generates a drop down for integer fields with a range
    choices = []
    for i in range(start, finish + 1):
        choice = (i, str(i))
        choices.append(choice)
    return choices

class Tag(models.Model):
    tag_description = models.CharField(
            max_length=100,
            primary_key=True,
            help_text='A high level descriptor for a project eg. Web App')

    def __str__(self): # To give an easier represenation when iterating
        return self.tag_description

class Module(models.Model):
    module_code = models.CharField(
            max_length=100,
            primary_key=True,
            help_text='UCL Module Code eg. COMP101P')

    def __str__(self):
        return self.module_code

class Student(models.Model):
    student_code = models.CharField(
            max_length=10,
            primary_key=True,
            help_text='UCL Student Number');
    forename = models.CharField(
            max_length=100,
            help_text='Student Forename')
    surname = models.CharField(
            max_length=100,
            help_text='Student Surname')
    email = models.CharField(
            max_length=100,
            help_text='Student Email')
    previous_leader = models.IntegerField(
            choices=get_integer_choices(0, MAX_TEAM_LEADER),
            default=0,
            validators=[MaxValueValidator(MAX_TEAM_LEADER), MinValueValidator(0)],
            help_text='Number of previous team leader roles')
    exam_results = models.DecimalField(
            default=Decimal(0.00),
            max_digits=5, # Only allow up to 100 with 2dp precision
            decimal_places=2,
            validators=[MaxValueValidator(100)],
            help_text='Combined previous results as a percentage')
    tag_like_1 = models.ForeignKey(
            Tag,
            related_name='tag_like_1',
            on_delete=models.CASCADE,
            null=True,
            help_text='Student\'s First Preference')
    tag_like_2 = models.ForeignKey(
            Tag,
            related_name='tag_like_2',
            on_delete=models.CASCADE,
            null=True,
            help_text='Student\'s Second Preference')
    tag_like_3 = models.ForeignKey(
            Tag,
            related_name='tag_like_3',
            on_delete=models.CASCADE,
            null=True,
            help_text='Student\'s Third Preference')
    tag_dislike_1 = models.ForeignKey(
            Tag,
            related_name='tag_dislike_1',
            on_delete=models.CASCADE,
            null=True,
            help_text='Student\'s Least Preference')
    student_modules = models.ManyToManyField(
            'Module',
            help_text='Modules the student is enrolled in')

    def get_absolute_url(self):
        # Returns the URL to the form where tags can be updated
        return reverse('matchingsystem:student_form', args=[str(self.student_code)])

    def __str__(self):
        return self.surname + ", " + self.forename

class Project(models.Model):
    # Uses default primary key (id)
    # These fields were provided by IXN
    project_title = models.CharField(
            max_length=200,
            help_text='A question or problem')
    project_background = models.CharField(
            max_length=500,
            help_text='Description of your company and its background')
    project_objectives = models.CharField(
            max_length=500,
            help_text='One line version of the project objectives')
    project_description = models.CharField(
            max_length=500,
            help_text='Details of the project')
    project_dataset = models.CharField(
            max_length=500,
            help_text='Descriptions of the dataset to be used')
    project_resources = models.CharField(
            max_length=500,
            help_text='Any additional resources that might be of interest')
    project_mentors = models.CharField(
            max_length=500,
            help_text='Names of mentors')

    # These fields are needed for matching - filled in by admin
    project_complexity = models.IntegerField(
            choices=get_integer_choices(1, MAX_PROJECT_COMPLEXITY),
            default=1,
            validators=[MaxValueValidator(MAX_PROJECT_COMPLEXITY), MinValueValidator(1)],
            help_text='Rating of the project difficulty from 1 to 5')
    project_module = models.ForeignKey(
            Module,
            on_delete=models.CASCADE,
            help_text='The module the project is to be matched with')
    project_tags = models.ManyToManyField(
            'Tag',
            help_text='The descriptors of the project')
    project_valid = models.BooleanField(
            default=False,
            help_text='Is the project suitable for matching')

    def __str__(self):
        return self.project_title
