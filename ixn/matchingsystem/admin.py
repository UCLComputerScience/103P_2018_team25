from django.contrib import admin
from .models import Tag, Project, Student, Module, StudentModule

# Add the forms to edit database structure
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Module)
