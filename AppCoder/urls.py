from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView


urlpatterns = [
        path("crear_curso/", crear_curso),
        path("listar_cursos/", listar_cursos),
        path("profesores/", profesores, name="profesores"),
        path("estudiantes/", estudiantes, name="estudiantes"),
        path("cursos/", cursos, name="cursos"),
        path("entregables/", entregables, name="entregables"),
        path("busquedaComision/", busquedaComision, name="busquedaComision"),
        path("buscar/", buscar, name="buscar"),

        path("eliminarProfesor/<id>", eliminarProfesor, name="eliminarProfesor"),
        path("editarProfesor/<id>", editarProfesor, name="editarProfesor"),

        path("estudiante/list/", EstudianteList.as_view(), name="estudiante_list"),
        path('estudiante/nuevo/', EstudianteCreacion.as_view(), name='estudiante_crear'),
        path('estudiante/<pk>', EstudianteDetalle.as_view(), name='estudiante_detalle'),
        path('estudiante/borrar/<pk>', EstudianteDelete.as_view(), name='estudiante_borrar'),
        path('estudiante/editar/<pk>', EstudianteUpdate.as_view(), name='estudiante_editar'),


        #LOGIN LOGOUT REGISTER

        path('login/', login_request, name='login'),
        path('register/', register, name='register'),
        path('logout/', LogoutView.as_view(), name='logout'),
    

]