from urllib import request

from django.shortcuts import get_object_or_404, render
from .models import Alumnos, ComentarioContacto,Archivos
from .forms import FromArchivos
from .forms import ComentarioContactoForm
from django.shortcuts import get_list_or_404
import datetime
from django.contrib import messages


# Create your views here.
def registros(request):
    alumnos = Alumnos.objects.all()

    return render(request,"registros/principal.html",{'8A':alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #inserta
            comentarios = ComentarioContacto.objects.all()
            return render(request,'registros/consultaComentario.html',{'comentarios':comentarios})

    form = ComentarioContactoForm()
#Si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'registros/contacto.html',{'form': form})


def consultaComentarios(request):
    comentarios = ComentarioContacto.objects.all()
    return render(request,'registros/consultaComentario.html',{'comentarios':comentarios})

def eliminarComentarioContacto(request, id,
        confirmacion = 'registros/confirmarEliminacion.html'):
    comentarios = get_list_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentarios[0].delete()
        comentarios= ComentarioContacto.objects.all()
        return render(request,'registros/consultaComentario.html',{'comentarios':comentarios})
    
    return render(request, confirmacion, {'comentario': comentarios})
    
def consultaComentarioIndividual(request, id):
        comentario = ComentarioContacto.objects.get(id=id)
        #get permite establecer una condicionante a la consulta y recuperar el objeto
        #del modelo que cumple la condicion(registro de la tabla ComentarioContacto .
        #get emplea cuando se sabe que se recuperara un solo registro, si se recuperan varios se genera una excepcion MultipleObjectsReturned
        return render(request,'registros/formEditarComentario.html',{'comentario':comentario})
#indicamos el lugar donde se renderizara el formulario de edicion y se envia el comentario recuperado para mostrar sus datos en el formulario

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #Referenciamos que el elemento del formulario permanece al comentario ya existente
    if form.is_valid():
        form.save()
        comentarios = ComentarioContacto.objects.all()
        return render(request,'registros/consultaComentario.html',{'comentarios':comentarios})
    return render(request,'registros/formEditarComentario.html',{'comentarios': comentarios})



def consultar1(request):
    #con una sola condicion 
    alumnos = Alumnos.objects.filter(carrera='TI')
    return render(request,"registros/consultas.html",{'8A':alumnos})    

def consultar2(request):
    #con una sola condicion 
    alumnos = Alumnos.objects.filter(carrera='TI').filter(turno='Matutino')
    return render(request,"registros/consultas.html",{'8A':alumnos})    

def consultar3(request):
    #con una sola condicion 
    alumnos = Alumnos.objects.all().only('matricula','nombre','carrera','turno','imagen')
    return render(request,"registros/consultas.html",{'8A':alumnos})    


def consultar4(request):
    #con una sola condicion 
    alumnos = Alumnos.objects.filter(turno__contains='Vesp')
    return render(request,"registros/consultas.html",{'8A':alumnos})

def consultar5(request):
    #con una sola condicion 

    alumnos = Alumnos.objects.filter(nombre__in=['Juan','Ana'])
    return render(request,"registros/consultas.html",{'8A':alumnos})   

def consultar6(request):
    fechaInicio = datetime.date(2026,2,13)
    fechaFin = datetime.date(2026,3,12)
    alumnos = Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'8A':alumnos})  

def consultar7(request):
    alumnos = Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'8A':alumnos})

def archivos(request):
    if request.method == 'POST':
        form = FromArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            archivo = request.FILES.get('archivo')

            insert = Archivos(
                titulo=titulo,
                descripcion=descripcion,
                archivo=archivo
            )
            insert.save()

            return render(request, 'registros/archivos.html')
        else:
            messages.error(request, "Error al procesar el formulario")

    else:
        return render(request, 'registros/archivos.html', {'archivo': Archivos})
    
def consultasSQL(request):
    alumnos = Alumnos.objects.raw('SELECT  id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera = "TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html",{'8A':alumnos})    
#########################################################################################################

def contacto(request):
    return render(request,"registros/contacto.html")