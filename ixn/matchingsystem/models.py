from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# These are the models to define database structure (tables, relationships)

class Tag(models.Model):
    # Uses default primary key (id)
    tag_description = models.CharField(max_length=100) # Length to be changed

    def __str__(self): # To give an easier represenation when iterating
        return self.tag_description

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True); # TODO How long can id be?
    tag_like_1 = models.ForeignKey(Tag, related_name='tag_like_1', on_delete=models.CASCADE)
    tag_like_2 = models.ForeignKey(Tag, related_name='tag_like_2', on_delete=models.CASCADE)
    tag_like_3 = models.ForeignKey(Tag, related_name='tag_like_3', on_delete=models.CASCADE)
    tag_dislike_1 = models.ForeignKey(Tag, related_name='tag_dislike_1', on_delete=models.CASCADE)
    previous_leader = models.IntegerField(
            default=0,
            validators=[MaxValueValidator(3), MinValueValidator(0)])
    # TODO Add other factors as they become clearer - work experiance etc

    def __str__(self):
        return self.student_id

class Project(models.Model):
    # Uses default primary key (id)
    project_name = models.CharField(max_length=200) # Length to be changed
    project_description = models.CharField(max_length=500)
    project_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    project_complexity = models.IntegerField(
            default=1,
            validators=[MaxValueValidator(5), MinValueValidator(1)])
    # TODO add other factors as they become clearer

    def __str__(self):
        return self.project_name

#TODO
# store exam data imported from script
# store modules
# store final results
