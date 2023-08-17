from django.shortcuts import render
from .models import Curso, Profesor, Estudiante
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def crear_curso(request):

    nombre_curso="Programacion Basica"
    comision_curso=999888
    print("creando curso")
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado: {curso.nombre} - {curso.comision}"
    return HttpResponse(respuesta)


def listar_cursos(request):
    cursos=Curso.objects.all()
    respuesta=""
    for curso in cursos:
        respuesta+=f"{curso.nombre} - {curso.comision}<br>"
    return HttpResponse(respuesta)


def inicio(request):
    return render(request,"AppCoder/inicio.html")

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

def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    formulario_profesor=ProfesorForm()
    mensaje="Profesor eliminado"
    return render(request,"AppCoder/profesores.html", {"mensaje":mensaje, "formulario":formulario_profesor, "profesores":profesores})

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

class EstudianteCreacion(CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(DeleteView):#vista usada para ELIMINAR
    model=Estudiante
    success_url= reverse_lazy("estudiante_list")

class EstudianteUpdate(UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']


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


def estudiantes(request):
    return render(request,"AppCoder/estudiantes.html")



def entregables(request):
    return render(request,"AppCoder/entregables.html")


def busquedaComision(request):
    return render(request,"AppCoder/busquedaComision.html")

def buscar(request):
    comision=request.GET["comision"]
    if comision!="":
        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request,"AppCoder/resultadosBusqueda.html", {"cursos":cursos})
    else:
        return render(request,"AppCoder/busquedaComision.html", {"mensaje":"che! no me ingresaste nada!!"})
        