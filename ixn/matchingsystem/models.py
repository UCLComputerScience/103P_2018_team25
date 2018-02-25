from django.db import models

# These are the models to define database structure, they can be easily changed and the database will reflect this
# So makes adding / removing features easy

class Tag(models.Model):
    # Default primary key is provided
    tag_description = models.CharField(max_length=100) # Length to be changed
