from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# These are the models to define database structure (tables, relationships)
# TODO lengths of char fields

MAX_TEAM_LEADER = 3
MAX_PROJECT_COMPLEXITY = 5

class Tag(models.Model):
    tag_description = models.CharField(max_length=100, primary_key=True)

    def __str__(self): # To give an easier represenation when iterating
        return self.tag_description

class Module(models.Model):
    module_code = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.module_code

class Student(models.Model): # Store all data and then bind csv row to this?
    student_code = models.CharField(max_length=10, primary_key=True);
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    previous_leader = models.IntegerField(
            default=0,
            validators=[MaxValueValidator(MAX_TEAM_LEADER), MinValueValidator(0)])
    exam_results = models.DecimalField(
            default=Decimal(0.00),
            max_digits=5, # Only allow up to 100 with 2dp precision
            decimal_places=2,
            validators=[MaxValueValidator(100)])
    tag_like_1 = models.ForeignKey(
            Tag,
            related_name='tag_like_1',
            on_delete=models.CASCADE,
            null=True)
    tag_like_2 = models.ForeignKey(
            Tag,
            related_name='tag_like_2',
            on_delete=models.CASCADE,
            null=True)
    tag_like_3 = models.ForeignKey(
            Tag,
            related_name='tag_like_3',
            on_delete=models.CASCADE,
            null=True)
    tag_dislike_1 = models.ForeignKey(
            Tag,
            related_name='tag_dislike_1',
            on_delete=models.CASCADE,
            null=True)
#modules = models.ManyToManyField('Module')

    def __str__(self):
        return self.surname + ", " + self.forename

class Project(models.Model):
    # Uses default primary key (id)
    project_title = models.CharField(max_length=200) # These were provided by IXN
    project_background = models.CharField(max_length=500)
    project_objectives = models.CharField(max_length=200)
    project_description = models.CharField(max_length=500)
    project_dataset = models.CharField(max_length=500)
    project_resources = models.CharField(max_length=500)
    project_mentors = models.CharField(max_length=200)

    project_complexity = models.IntegerField( # These are needed for matching
            default=1,
            validators=[MaxValueValidator(MAX_PROJECT_COMPLEXITY), MinValueValidator(1)])
    project_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    project_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    project_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.project_title

class StudentModule(models.Model):
    # Uses default primary key (id)
    student = models.ForeignKey(Student)
    module = models.ForeignKey(Module)

    def __str__(self):
        return self.student.__str__() + ":" + self.module.__str__()
