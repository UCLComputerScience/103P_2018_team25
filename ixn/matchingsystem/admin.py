from django.contrib import admin
from .models import Tag, Project, Student, Module

# Customise the admin area

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'surname', 'forename')
    list_filter = ['student_modules']
    search_fields = ['student_code', 'surname', 'forename']

    fieldsets = [
        ('Student Information', {'fields': ['student_code', 'forename', 'surname', 'exam_results', 'student_modules']}),
        ('Matching Information', {'fields': ['tag_like_1', 'tag_like_2', 'tag_like_3', 'tag_dislike_1', 'previous_leader']}),
    ]
    filter_horizontal = ('student_modules',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'project_module', 'project_valid')
    list_filter = ['project_module', 'project_tags', 'project_valid']
    search_fields = ['project_title']

    fieldsets = [
        ('Project Information', {'fields': ['project_title', 'project_background', 'project_objectives', 'project_description', 'project_dataset', 'project_resources', 'project_mentors']}),
        ('Matching Information', {'fields': ['project_valid', 'project_tags', 'project_module', 'project_complexity']}),
    ]
    filter_horizontal = ('project_tags',)

# Add the forms to edit database structure
admin.site.register(Project, ProjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tag)
admin.site.register(Module)
