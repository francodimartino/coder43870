from django.shortcuts import render
from .models import Curso, Profesor, Estudiante
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm, RegistroUsuarioForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import   AuthenticationForm, UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin #para vistas basadas en clases CLASS   
from django.contrib.auth.decorators import login_required #para vistas basadas en funciones DEF  

# Create your views here.
def crear_curso(request):

    nombre_curso="Programacion Basica"
    comision_curso=999888
    print("creando curso")
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado: {curso.nombre} - {curso.comision}"
    return HttpResponse(respuesta)

@login_required
def listar_cursos(request):
    cursos=Curso.objects.all()
    respuesta=""
    for curso in cursos:
        respuesta+=f"{curso.nombre} - {curso.comision}<br>"
    return HttpResponse(respuesta)


def inicio(request):
    return render(request,"AppCoder/inicio.html")
@login_required
def profesores(request):
    if request.method=="POST":
        form=ProfesorForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre=info["nombre"]
            apellido=info["apellido"]
            email=info["email"]
            profesion=info["profesion"]
            profesor=Profesor(nombre=nombre,apellido=apellido,email=email,profesion=profesion)
            profesor.save()
            mensaje="Profesor creado"
            
            
        else:
            mensaje="Datos invalidos"
        profesores=Profesor.objects.all()
        formulario_profesor=ProfesorForm()
        return render(request,"AppCoder/profesores.html", {"mensaje":mensaje, "formulario":formulario_profesor, "profesores":profesores})
    else:

        formulario_profesor=ProfesorForm()
        profesores=Profesor.objects.all()

    return render(request,"AppCoder/profesores.html", {"formulario": formulario_profesor, "profesores":profesores})
@login_required
def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    formulario_profesor=ProfesorForm()
    mensaje="Profesor eliminado"
    return render(request,"AppCoder/profesores.html", {"mensaje":mensaje, "formulario":formulario_profesor, "profesores":profesores})
@login_required
def editarProfesor(request, id):

    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form=ProfesorForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]
           
            profesor.save()
            mensaje="Profesor editado!"
            profesores=Profesor.objects.all()
            formulario_profesor=ProfesorForm()
            return render(request,"AppCoder/profesores.html", {"mensaje":mensaje, "formulario":formulario_profesor, "profesores":profesores})

    else:
        
        formulario_profesor=ProfesorForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
        return render(request,"AppCoder/editarProfesor.html", {"formulario":formulario_profesor, "profesor":profesor})


class EstudianteList(ListView):#vista usada para LISTAR
    model= Estudiante
    template_name= "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(LoginRequiredMixin, DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(LoginRequiredMixin,DeleteView):#vista usada para ELIMINAR
    model=Estudiante
    success_url= reverse_lazy("estudiante_list")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']

@login_required
def cursos(request):
    if request.method=="POST":
        form=CursoForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre=info["nombre"]
            comision=info["comision"]
            curso=Curso(nombre=nombre,comision=comision)
            curso.save()
            return render(request,"AppCoder/cursos.html", {"mensaje":"Curso creado"})
        return render(request,"AppCoder/cursos.html", {"mensaje":"Datos invalidos"})
    else:
        formulario_curso=CursoForm()
        return render(request,"AppCoder/cursos.html", {"formulario": formulario_curso})

@login_required
def estudiantes(request):
    return render(request,"AppCoder/estudiantes.html")


@login_required
def entregables(request):
    return render(request,"AppCoder/entregables.html")

@login_required
def busquedaComision(request):
    return render(request,"AppCoder/busquedaComision.html")

@login_required
def buscar(request):
    comision=request.GET["comision"]
    if comision!="":
        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request,"AppCoder/resultadosBusqueda.html", {"cursos":cursos})
    else:
        return render(request,"AppCoder/busquedaComision.html", {"mensaje":"che! no me ingresaste nada!!"})
        

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)#verifica si el usuario existe, si existe, me devuelve el usuario, y si no me devuelve None
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente"})
            else:
                return render(request,"AppCoder/login.html", {"form":form, "mensaje":"Datos invalidos"})
        else:
            return render(request,"AppCoder/login.html", {"form":form, "mensaje":"Datos invalidos"})
    else:
        form=AuthenticationForm()
        return render(request,"AppCoder/login.html", {"form":form})

def register(request):
    if request.method=="POST":
        form=RegistroUsuarioForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre_usuario=info["username"]
            form.save()#grabo usuario en base de datos
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {nombre_usuario} creado correctamente"})
        else:
            return render(request,"AppCoder/register.html", {"form":form, "mensaje":"Datos invalidos"})

    else:
        form=RegistroUsuarioForm()
        return render(request,"AppCoder/register.html", {"form":form})
