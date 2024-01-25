from django.contrib import admin
from .models import Task

# Register your models here.
#esto es para visualizar los campos que se generan automatiamente y son solo de lectura
# en este caso la face de cracion
# this class is for the view data only read
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
#con esto visualizo los datos en la parte de administradorvvvvvvvvvvvvvvvvvvvvvgfv    
admin.site.register(Task,TaskAdmin)

