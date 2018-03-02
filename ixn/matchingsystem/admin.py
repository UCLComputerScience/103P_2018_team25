from django.contrib import admin
from .models import Tag, Project, Student, Module, StudentModule

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Module)
admin.site.register(StudentModule) # To remove after debugging
