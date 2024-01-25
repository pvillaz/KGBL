from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomplete = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #esto es para visualizar las campos de la tabla en la parte de administrador
    #this part is for view the title an description in admin page
    
    def __str__(self):
        return self.title + '- by ' + self.user.username

