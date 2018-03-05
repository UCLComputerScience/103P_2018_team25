from django.contrib import admin
from .models import Tag, Project, Student, Module, StudentModule

# Customise the admin area

class StudentModuleInline(admin.TabularInline):
    # Allows modules to be edited in the student form
    model = StudentModule
    extra = 0

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'surname', 'forename')
#list_filter = ['modules']
    search_fields = ['student_code', 'surname', 'forename']

    fieldsets = [
        ('Student Information', {'fields': ['student_code', 'forename', 'surname', 'exam_results']}),
        ('Matching Information', {'fields': ['tag_like_1', 'tag_like_2', 'tag_like_3', 'tag_dislike_1', 'previous_leader']}),
    ]
    inlines = [StudentModuleInline]

class ProjectAdmin(admin.ModelAdmin): # Make fields easier to see?
    list_display = ('project_title', 'project_module', 'project_tag', 'project_valid')
    list_filter = ['project_module', 'project_tag', 'project_valid']
    search_fields = ['project_title']

    fieldsets = [
        ('Project Information', {'fields': ['project_title', 'project_background', 'project_objectives', 'project_description', 'project_dataset', 'project_resources', 'project_mentors']}),
        ('Matching Information', {'fields': ['project_valid', 'project_tag', 'project_module', 'project_complexity']}),
    ]

# Add the forms to edit database structure
admin.site.register(Project, ProjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tag)
admin.site.register(Module)
