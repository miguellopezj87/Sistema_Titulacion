"""Sistema_Titulacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from titulacion import views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.mostrarLogin),
    path('login', views.iniciarSesion),
    path('logout', views.cerrarSesion),
    path('menu_admin', views.mostrarMenuAdmin),
    path('form_reg_usu', views.mostrarFormRegistrarUsuario),
    path('registrar_usuario', views.registrarUsuario),
    path('form_act_usu/<int:id>', views.mostrarFormActualizarUsuario),
    path('actualizar_usuario/<int:id>', views.actualizarUsuario),
    path('deshabilitar_usuario/<int:id>', views.deshabilitarUsuario),

    path('cargar_archivo', views.cargarArchivo),
    path('subir_archivo', views.subirArchivo),
    
    path('menu_anfitrion', views.mostrarMenuAnfitrion),
    path('gestionar_recepcion', views.gestionarRecepcion),
    
    path('cargar_titulados/<mes>/<yea>', views.cargarTitulados),
    
    path('gestionar_recepcion_mensual/<yearTitulacion>', views.gestionarRecepcionMensual),
    
    path('guardar_asistencia_titulados/<ide>/<mes>/<yea>/<sit>/<ninv>/<ff>/<msgerror>', views.guardar_asistencia_titulados),

    path('gestionar_recepcion_menadm/<yearTitulacion>', views.gestionarRecepcionMenAdm),    
    path('cargar_titulados_adm/<mes>/<yea>', views.cargarTituladosAdm),
    path('guardar_asistencia_titulados_adm/<ide>/<mes>/<yea>/<sit>/<ninv>/<ff>/<msgerror>', views.guardar_asistencia_titulados_adm),
    path('cambiar_estado_fecha_adm/<ff>/<op>', views.cambiar_estado_fecha_adm),
    path('cambiar_estado_mes_adm/<mes>/<yea>/<op>', views.cambiar_estado_mes_adm),
    
    path('menu_organizador', views.mostrarMenuOrganizador),
    
    path('delete_year_adm/<year>/<pasw>', views.delete_year_adm),

    path('gestionar_recepcion_org', views.gestionar_recepcion_org),
    
    path('gestionar_recepcion_menorg/<yearTitulacion>', views.gestionar_recepcion_menorg),
    path('cargar_titulados_org/<mes>/<yea>', views.cargarTituladosOrg),
    path('cargar_titulados_org_det/<mes>/<yea>', views.cargarTituladosOrgDet),

    path('ver_asistentes_adm', views.ver_asistentes_adm),
    path('ver_asistentes_menadm/<yearTitulacion>', views.ver_asistentes_menadm),
    path('ver_asistentes_menadm_cargar/<mes>/<yea>', views.ver_asistentes_menadm_cargar),
    path('ver_asistentes_menadm_cargar_det/<mes>/<yea>', views.ver_asistentes_menadm_cargar_det),

    path('mostrar_gestionar_libreto_adm', views.mostrarFormGestionarLibretoAdm),
    path('guardar_libreto_adm', views.guardarLibretoAdm),

    path('menu_locutor', views.mostrarMenuLocutor),
    path('ver_libreto_loc', views.ver_libreto_loc),
    path('ver_libreto_menloc/<yearTitulacion>', views.ver_libreto_menloc),
    path('ver_libreto_menloc_cargar/<mes>/<yea>', views.ver_libreto_menloc_cargar),
    path('ver_libreto_menloc_cargar_det/<mes>/<yea>', views.ver_libreto_menloc_cargar_det),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
