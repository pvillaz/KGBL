#from django.forms import ModelForm
from django import forms
from .models import Task


#esto es para crear el formulario de la tabla para ingresar los datos
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        #estilizamos el formulario con esta etiqueta widgets
        widgets= {
            'title': forms.TextInput(attrs= {'class':'form-control','placeholder':'write a title'}),
            'description': forms.Textarea(attrs= {'class':'form-control','placeholder':'write a description'}),
            'important': forms.CheckboxInput(attrs= {'class':'form-check-input m-auto'}),
            }