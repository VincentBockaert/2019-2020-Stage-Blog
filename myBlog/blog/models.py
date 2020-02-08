from django.db import models
from django.utils import timezone
# Create your models here.

class Author(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Blog(models.Model):
    pub_date = models.DateTimeField('Date published')
    title = models.CharField(max_length=200)
    description = models.TextField(default="No description was found.")
    content = models.TextField()
    last_edited_date = models.DateTimeField('Last edited on',default=timezone.now())

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title