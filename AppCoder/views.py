from django.shortcuts import render
from .models import Curso, Profesor
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm

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
            formulario_profesor=ProfesorForm()
            return render(request,"AppCoder/profesores.html", {"mensaje":"Profesor creado", "formulario":formulario_profesor})
        else:
            return render(request,"AppCoder/profesores.html", {"mensaje":"Datos invalidos"})
    else:

        formulario_profesor=ProfesorForm()

    return render(request,"AppCoder/profesores.html", {"formulario":formulario_profesor})

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
        