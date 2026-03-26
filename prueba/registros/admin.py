from urllib import request

from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto


class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created','updated')
    list_display = ('matricula','nombre','carrera','turno','created')
    search_fields = ('matricula','nombre','carrera','turno')
    date_hierarchy = 'created'
    list_filter = ('carrera','turno')
    list_display_links = ('matricula','nombre')
    list_per_page = 3
    
    
    def get_readonly_fields(self, request, obj=None):
        #si el usuario pertenece al grupo de permisos "Usuarios"
        if request.user.groups.filter(name="Usuarios").exists():
            #Bloquea los campos
            return ('matricula','carrera','turno')
        #Cualquier otro usuario que no pertenece al grupo "Usuario"
        else:
            return ('created','updated')
        

    def get_readonly_fields(self, request, obj=None):

        if request.user.groups.filter(name="EditoresAlumnos").exists():
        # Solo puede editar nombre, carrera y fotografia
         return ('matricula','turno')

        else:
         return ('created','updated')   
        
admin.site.register(Alumnos, AdministrarModelo)

class AdministrarComentario(admin.ModelAdmin):
    list_display =('id','coment')
    search_fields=('id','created')
    date_hierarchy = 'created'
    readonly_fields = ('created','id')

admin.site.register(Comentario, AdministrarComentario)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id', 'mensaje')
    search_fields = ('id','created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')

    
admin.site.register(ComentarioContacto, AdministrarComentariosContacto)