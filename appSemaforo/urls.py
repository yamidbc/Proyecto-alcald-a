from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django import views     #  <<==========
from django.urls import path, include
from appSemaforo import views 
from appSemaforo.views import ListadoUsuario,RegistrarUsuario, ActualizarUsuario,EliminarUsuario,ListadoLineaE,RegistrarLineaE,ActualizarLineaE, EliminarLineaE,ListadoPilarS,RegistrarPilarS,ActualizarPilarS,EliminarPilarS,ListadoPrograma,RegistrarPrograma,ActualizarPrograma, EliminarPrograma, ListadoProducto,RegistrarProducto,ActualizarProducto,EliminarProducto,RegistrarUsuarioPublico,ListadoIndicadorProducto,RegistrarIndicadorProducto,ActualizarIndicadorProducto,EliminarIndicadorProducto,historico_producto,PerfilUsuario,reprogramar_vigencia,ListadoContrato,RegistrarContrato,ActualizarContrato,EliminarContrato
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

class LogoutViewPersonalizada(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('login')  # Redirige a la página de login después de cerrar sesión

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Sesión cerrada correctamente')
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('logout/', views.LogoutViewPersonalizada.as_view(), name='logout'),
    path('grafico_barras/', views.grafico_barras, name='grafico_barras'),
     path('home/', login_required(views.index), name="home"),
    path('listar/', login_required(ListadoUsuario.as_view()), name='listar'),
    path('agregar/', login_required(RegistrarUsuario.as_view()), name='registrar_usuario'),
    path('modificar/<int:pk>/', login_required(ActualizarUsuario.as_view()), name='modificar'),
    path('eliminar/<int:pk>/', login_required(EliminarUsuario.as_view()), name="eliminar"),
    path('registrar/', RegistrarUsuarioPublico.as_view(), name='registrar_publico'),
    path('perfil/', login_required(PerfilUsuario.as_view()), name='perfil'),
    
    # CRUD linea estrategica URLS
    path('listarLinea/', login_required(ListadoLineaE.as_view()), name='listar_LineaE'),
    path('agregarLinea/', login_required(RegistrarLineaE.as_view()), name='agregar_LineaE'),
    path('actualizarLineaE/<int:pk>/', login_required(ActualizarLineaE.as_view()), name='actualizar_LineaE'),
    path('eliminarLineaE/<int:pk>/', login_required(EliminarLineaE.as_view()), name='eliminar_LineaE'),
    
    # CRUD pilar sectorial URLS
    path('listarPilarS/', login_required(ListadoPilarS.as_view()), name='listar_pilarS'),
    path('agregarPilarS/', login_required(RegistrarPilarS.as_view()), name='agregar_pilarS'),
    path('actualizarPilarS/<int:pk>/', login_required(ActualizarPilarS.as_view()), name='actualizar_pilarS'),
    path('eliminarPilarS/<int:pk>/', login_required(EliminarPilarS.as_view()), name='eliminar_pilarS'),
    
    # CRUD programa URLS
    path('listarPrograma/', login_required(ListadoPrograma.as_view()), name='listar_programa'),
    path('agregarPrograma/', login_required(RegistrarPrograma.as_view()), name='agregar_programa'),
    path('actualizarPrograma/<int:pk>/', login_required(ActualizarPrograma.as_view()), name='actualizar_programa'),
    path('eliminarPrograma/<int:pk>/', login_required(EliminarPrograma.as_view()), name='eliminar_programa'),
    #CRUD contrato URLS
    path('listarContrato/', login_required(ListadoContrato.as_view()), name='listar_Contrato'),
    path('agregarContrato/', login_required(RegistrarContrato.as_view()), name='agregar_Contrato'),
    path('actualizarContrato/<int:pk>/', login_required(ActualizarContrato.as_view()), name='actualizar_Contrato'),
    path('eliminarContrato/<int:pk>/', login_required(EliminarContrato.as_view()), name='eliminar_Contrato'),
    
    # CRUD producto URLS
    path('listarProducto/', login_required(ListadoProducto.as_view()), name='listar_producto'),
    path('agregarProducto/', login_required(RegistrarProducto.as_view()), name='agregar_producto'),
    path('actualizarProducto/<int:pk>/', login_required(ActualizarProducto.as_view()), name='actualizar_producto'),
    path('eliminarProducto/<int:pk>/', login_required(EliminarProducto.as_view()), name='eliminar_producto'),
    path('detalle_producto/<int:pk>/', views.DetalleProducto.as_view(), name='detalle_producto'),
    path('detalle_producto/<int:pk>/', views.DetalleProducto.as_view(), name='detalle_producto'),
    path('descargar-archivo/<int:pk>/', login_required(views.descargar_archivo), name='descargar_archivo'),
    path('descargar-archivo2/<int:pk>/', login_required(views.descargar_archivo_soporte_2), name='descargar_archivo2'),
    path('obtener_datos_grafico_torta/', views.obtener_datos_grafico_torta, name='obtener_datos_grafico_torta'),
    path('obtener_datos_grafico_linea/', views.obtener_datos_grafico_linea, name='obtener_datos_grafico_linea'),
    path('reprogramar_vigencia/<pk>/', views.reprogramar_vigencia, name='reprogramar_vigencia'),
    
    # CRUD indidacador_producto URLS
    path('indicador_producto/listar/', login_required(ListadoIndicadorProducto.as_view()), name='listar_indicador_producto'),
    path('indicador_producto/registrar/',login_required( RegistrarIndicadorProducto.as_view()), name='registrar_indicador_producto'),
    path('indicador_producto/actualizar/<int:pk>/',login_required( ActualizarIndicadorProducto.as_view()), name='actualizar_indicador_producto'),
    path('indicador_producto/eliminar/<int:pk>/', login_required(EliminarIndicadorProducto.as_view()), name='eliminar_indicador_producto'),
    
    # Historial
    path('historico_producto/', login_required(historico_producto.as_view()), name='historico_producto'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)