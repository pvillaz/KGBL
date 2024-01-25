from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
#importando el formulario que cree para las tareas
from .forms import TaskForm
#importando las tareas
from .models import Task
from django.utils import timezone
#esto es para proteger las paginas con usuarios autenticados
from django.contrib.auth.decorators import login_required

# Create your views here.

# metdodo para ir a la pagina principal

#pagina principal de la web
def home(request):
    return render(request, 'home.html')

# metodo para logearse al crear al usuario


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, "error": 'username already exist'})

    return render(request, 'signup.html', {'form': UserCreationForm, "error": 'password do not match'})
  # metodo para crear las tareas cuando se logea correctamente el usuario

#aqui podria usar tablas dinamicas
#metodo muestra solo tareas que aun no esta completadas
@login_required  #esto es para proteger la pagina solo a usuarios logeados
def tasks(request):
    #visualizando el listado de las tareas de la base de datos filtrando por usuario logeado con filter..
    tasks = Task.objects.filter(user=request.user,datecomplete__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks})

#metodo para listar las tareas que han sido completadas
@login_required
def tasks_completed(request):
    #visualizando el listado de las tareas de la base de datos filtrando por usuario logeado con filter..
    tasks = Task.objects.filter(user=request.user,datecomplete__isnull=False).order_by('-datecomplete')
    return render(request, 'tasks.html', {'tasks':tasks})


#funcion especial para creat la vista de tareas
#le paso elparametro personalizado TaskForm
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{'form': TaskForm})
    else:
        try:
            #print(request.POST)
            #AQUI GUARDAMOS LOS DATOS EN LA BASE DE DATOS
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
        
            return render(request, 'create_task.html',{'form': TaskForm,'error': 'Please provide valid data'})
        
#metodo o funcion  para buscar una sola tarea
@login_required
def task_detail(request, task_id):
    
   if request.method=='GET':
       task= get_object_or_404(Task,pk=task_id, user=request.user)
        #llenar un formukario para editar los valores de las tareas
       form = TaskForm(instance=task)
       return render(request,'task_detail.html',{'task':task, 'form':form})
    
   else:
       try:
            task= get_object_or_404(Task,pk=task_id, user=request.user)
            form= TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
       
       except ValueError:
           return render(request,'task_detail.html',{'task':task, 'form':form, 'error':'Error updating task'})
    
#FUNCION PARA COMPLETAR TARREAS
@login_required
def complete_task(request,task_id):   
    task= get_object_or_404(Task,pk=task_id, user=request.user) 
    if request.method=='POST':
        task.datecomplete = timezone.now()
        task.save()
        return redirect('tasks')
    
    
#funcion para eliminar
@login_required
def delete_task(request,task_id):   
    task= get_object_or_404(Task,pk=task_id, user=request.user) 
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
    
      
@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            login(request,user)
            return redirect('tasks')
      #  return render(request, 'signin.html', {'form': AuthenticationForm})
