from django.db import models
from matchingsystem.models import Project
'''
class ClientProfile(models.Model): # To enable clients linked to projects TODO check if you can just use foreign key in project
    user = models.OneToOneFields(User, on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)

@reciever(post_save, sender=User)
def update_client_profile(sender, instance, created, **kwargs):
    if(created):
        ClientProfile.objects.create(user=instance) # Add objects here?
    instance.profile.save()'''
