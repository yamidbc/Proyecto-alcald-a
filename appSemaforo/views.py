from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import Trunc
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Case, When, IntegerField
from django.template.loader import get_template
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_GET
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseServerError
from django.template.loader import get_template
import threading
from django.contrib.auth import get_user

from django.template.loader import get_template
import uuid
import calendar
import os
import json
from .utils import generate_unique_filename
from decimal import Decimal
from .models import Usuario,Linea_estrategica,Pilar_sectorial,Programa,Producto,Indicador_Producto,HistoricoProducto,Contrato
from .forms import FormularioUsuario, FormularioLineaE,FormularioPilarS,FormularioPrograma,ProductoForm,FormularioLogin, FormularioUsuarioPublico,IndicadorProductoForm,ReprogramarVigenciaForm,FormularioContrato
from datetime import datetime
from .utils import calcular_meses


def login_view(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request, 'Credenciales incorrectas')
        else:
            messages.error(request, 'Formulario inválido')
    else:
        form = FormularioLogin()

    return render(request, 'login.html', {'form': form})

class LogoutViewPersonalizada(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Sesión cerrada correctamente')
        return super().dispatch(request, *args, **kwargs)
@login_required
def index(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

@require_GET
def grafico_barras(request):
    try:
        datos = Usuario.objects.filter(usuario_activo=True).exclude(created_at__isnull=True).extra(
            select={'mes': "EXTRACT(MONTH FROM created_at)"}).values('mes').annotate(count=Count('id')).order_by('mes')
        
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        usuarios_por_mes = [0] * 12
        
        for d in datos:
            if d['mes'] is not None and isinstance(d['mes'], int) and 1 <= d['mes'] <= 12:
                usuarios_por_mes[d['mes']-1] = d['count']
        
        return JsonResponse({'xAxis': meses, 'series': usuarios_por_mes})
    except Exception as e:
        return JsonResponse({'error': str(e)})


#  <<========== CRUD DE USUARIOS


class ListadoUsuario(LoginRequiredMixin,ListView):
    model = Usuario
    template_name = 'Usuarios/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)

class RegistrarUsuario(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuarios/agregar.html'
    success_url = reverse_lazy('listar')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password1 = form.cleaned_data.get('password1')
            if password != password1:
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                return render(request, self.template_name, {'form': form})
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.set_password(password)
            nuevo_usuario.save()
            messages.add_message(request, messages.SUCCESS, 'Usuario creado con éxito')
            return redirect(self.success_url)
        else:
            messages.add_message(request, messages.ERROR, 'Error en el formulario')
            return render(request, self.template_name, {'form': form})
        
        
class ActualizarUsuario(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuarios/modificar.html'
    success_url = reverse_lazy('listar')

    def form_valid(self, form):
        print("Formulario válido")
        password = form.cleaned_data.get('password')
        password1 = form.cleaned_data.get('password1')
        if password != password1:
            messages.add_message(self.request, messages.ERROR, 'Las contraseñas no coinciden')
            return self.render_to_response(self.get_context_data(form=form))
        usuario = form.save(commit=False)
        usuario.set_password(password)
        try:
            usuario.save()
            print("Cambios guardados correctamente")
            messages.add_message(self.request, messages.SUCCESS, 'Usuario actualizado con éxito')
        except Exception as e:
            print("Error al guardar cambios:", e)
            messages.add_message(self.request, messages.ERROR, 'Error al actualizar usuario')
        return super().form_valid(form)

class EliminarUsuario(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('listar')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Producto.objects.filter(ID_usuarioPropietario=self.object.id).exists():
            messages.error(request, 'No se puede eliminar este usuario porque tiene dependencias con productos.')
            return redirect('listar')
        return super().get(request, *args, **kwargs)


class RegistrarUsuarioPublico(CreateView):
    model = Usuario
    form_class = FormularioUsuarioPublico
    template_name = 'Usuarios/registrar_publico.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password1 = form.cleaned_data.get('password1')
            if password != password1:
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                return render(request, self.template_name, {'form': form})
            usuario = form.save(commit=False)
            usuario.is_superuser = False
            usuario.set_password(password)
            usuario.usuario_activo = True
            usuario.is_guest = True
            usuario.save()
            messages.add_message(request, messages.SUCCESS, 'Usuario creado con éxito')
            return redirect(self.success_url)
        else:
            print(form.errors)  # Imprime los errores del formulario
            messages.add_message(request, messages.ERROR, 'Error en el formulario')
            return render(request, self.template_name, {'form': form})
    
    
class PerfilUsuario(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuarios/perfil.html'
    success_url = reverse_lazy('listar')

    def get_object(self, queryset=None):
        messages.add_message(self.request, messages.SUCCESS, 'información de perfil actualizada con éxito')
        return self.request.user

#  <<========== CRUD DE lINEA ESTRATEGICA

class ListadoLineaE(LoginRequiredMixin,ListView):
    model = Linea_estrategica
    template_name = 'LineaEstrategica/listar_LineaE.html'

    def get_queryset(self):
        return self.model.objects.all()
    

class RegistrarLineaE(LoginRequiredMixin,CreateView):
    model = Linea_estrategica
    form_class = FormularioLineaE
    template_name = 'LineaEstrategica/agregar_LineaE.html'
    success_url=reverse_lazy('listar_LineaE')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Línea estratégica creada con éxito')
        return redirect(self.success_url)
    def  form_invalid(self, form):
        return render(self.request,self.template_name,{'form':form})

class ActualizarLineaE(LoginRequiredMixin,UpdateView):
    model = Linea_estrategica
    form_class = FormularioLineaE
    template_name = 'LineaEstrategica/actualizar_LineaE.html'
    success_url = reverse_lazy('listar_LineaE')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Línea estratégica actualizada con éxito')
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})



class EliminarLineaE(LoginRequiredMixin, DeleteView):
    model = Linea_estrategica
    template_name = 'LineaEstrategica/eliminar_LineaE.html'
    success_url = reverse_lazy('listar_LineaE')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tiene_dependencias():
            messages.error(request, 'No se puede eliminar esta línea estratégica porque tiene dependencias con pilares sectoriales.')
            return redirect('listar_LineaE')
        return super().get(request, *args, **kwargs)
    
#  <<========== CRUD DE Contrato
class ListadoContrato(LoginRequiredMixin,ListView):
    model = Contrato
    template_name = 'Contrato/Listar_contrato.html'

    def get_queryset(self):
        return self.model.objects.all()
    

class RegistrarContrato(LoginRequiredMixin,CreateView):
    model = Contrato
    form_class = FormularioContrato
    template_name = 'Contrato/Crear_contrato.html'
    success_url=reverse_lazy('listar_Contrato')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Contrato creado con éxito')
        return redirect(self.success_url)
    def  form_invalid(self, form):
        return render(self.request,self.template_name,{'form':form})

class ActualizarContrato(LoginRequiredMixin,UpdateView):
    model = Contrato
    form_class = FormularioContrato
    template_name = 'Contrato/Crear_contrato.html'
    success_url = reverse_lazy('listar_Contrato')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Contrato actualizado con éxito')
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})



class EliminarContrato(LoginRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'Contrato/Crear_contrato.html'
    success_url = reverse_lazy('listar_Contrato')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tiene_dependencias():
            messages.error(request, 'No se puede eliminar este registro de contrato, porque tiene dependencias con productos existentes')
            return redirect('listar_Contrato')
        return super().get(request, *args, **kwargs)
    
    
def obtener_valor_contrato(request, pk):
    contrato = Contrato.objects.get(pk=pk)
    valor = contrato.valor
    return HttpResponse(valor, content_type='application/json')    

   
 #  <<========== CRUD DE Pilar Sectorial
 
class ListadoPilarS(LoginRequiredMixin,ListView):
    model = Pilar_sectorial
    template_name = 'PilarSectorial/listar_pilarS.html'

    def get_queryset(self):
        return self.model.objects.all()
    

class RegistrarPilarS(LoginRequiredMixin,CreateView):
    model = Pilar_sectorial
    form_class = FormularioPilarS
    template_name = 'PilarSectorial/agregar_pilarS.html'
    success_url=reverse_lazy('listar_pilarS')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Pilar sectorial creado con éxito')
        return redirect(self.success_url)
    def  form_invalid(self, form):
        return render(self.request,self.template_name,{'form':form})

class ActualizarPilarS(LoginRequiredMixin,UpdateView):
    model = Pilar_sectorial
    form_class = FormularioPilarS
    template_name = 'PilarSectorial/modificar_pilarS.html'
    success_url = reverse_lazy('listar_pilarS')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Pilar sectorial actualizado con éxito')
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class EliminarPilarS(LoginRequiredMixin, DeleteView):
    model = Pilar_sectorial
    template_name = 'PilarSectorial/eliminar_pilarS.html'
    success_url = reverse_lazy('listar_pilarS')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.programa_set.exists():
            messages.error(request, 'No se puede eliminar este pilar sectorial porque tiene dependencias con programas.')
            return redirect('listar_pilarS')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
    
 #  <<========== CRUD DE Programa
 
class ListadoPrograma(LoginRequiredMixin,ListView):
    model =Programa
    template_name = 'Programas/listar_programa.html'

    def get_queryset(self):
        return self.model.objects.all()
    



class RegistrarPrograma(LoginRequiredMixin,CreateView):
    model = Programa
    form_class = FormularioPrograma
    template_name = 'Programas/agregar_programa.html'
    success_url = reverse_lazy('listar_programa')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Programa creado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class ActualizarPrograma(LoginRequiredMixin,UpdateView):
    model = Programa
    form_class = FormularioPrograma
    template_name = 'Programas/modificar_programa.html'
    success_url = reverse_lazy('listar_programa')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Programa actualizado con éxito')
        form.save()
        
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class EliminarPrograma(LoginRequiredMixin, DeleteView):
    model = Programa
    template_name = 'Programas/eliminar_programa.html'
    success_url = reverse_lazy('listar_programa')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.producto_set.exists():
            messages.error(request, 'No se puede eliminar este programa porque tiene dependencias con productos.')
            return redirect('listar_programa')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.add_message(self.request, messages.SUCCESS, 'Programa eliminado con éxito')
        return response
    
    
 #  <<========== CRUD DE Producto

class DetalleProducto(DetailView):
    model = Producto
    template_name = 'producto/Ver_producto.html'
    context_object_name = 'producto'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    


class ListadoProducto(LoginRequiredMixin,ListView):
    model = Producto
    template_name = 'Producto/listar_producto.html'

    def get_queryset(self):
        return self.model.objects.filter(estado__in=['Activo', 'Inactivo', 'Activo_Reprogramado', 'Expirada'])
    
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = context['object_list']
        for producto in productos:
            producto.calificacion = producto.calcular_calificacion()
        return context


@require_GET 
def obtener_datos_grafico_torta(request):
    try:
        productos = Producto.objects.filter(estado__in=['Activo', 'Activo_Reprogramado'])

        iniciada = 0
        en_progreso = 0
        completada = 0
        no_iniciada = 0

        for producto in productos:
            if producto.status_progreso == 'Iniciada':
                iniciada += 1
            elif producto.status_progreso == 'En progreso':
                en_progreso += 1
            elif producto.status_progreso == 'Completada':
                completada += 1
            else:
                no_iniciada += 1

        datos = [
            {"value": iniciada, "name": "Iniciada"},
            {"value": en_progreso, "name": "En progreso"},
            {"value": completada, "name": "Completada"},
            {"value": no_iniciada, "name": "No iniciada"}
        ]

        return JsonResponse(datos, safe=False, content_type='application/json')
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_GET
def obtener_datos_grafico_linea(request):
    try:
        pagina = int(request.GET.get('pagina', 1))
    except ValueError:
        return JsonResponse({'error': 'La página debe ser un número entero'}, status=400)
    if pagina < 1:
        return JsonResponse({'error': 'La página debe ser un número entero positivo'}, status=400)
    productos = Producto.objects.filter(estado__in=['Activo', 'Activo_Reprogramado'])
    total_productos = productos.count()
    productos_paginados = productos[(pagina-1)*10:pagina*10]
    if not productos_paginados:
        return JsonResponse({'error': 'No hay productos para mostrar en esta página'}, status=404)
    datos = {
        'xAxis': [producto.Nombre_Producto for producto in productos_paginados],
        'series': [
            {'name': 'Progreso', 'data': [round(producto.Valor_actual / producto.Meta_Actual * 100, 1) for producto in productos_paginados]},
            {'name': 'Presupuesto Utilizado', 'data': [round(producto.Presupuesto_utilizado / producto.presupuesto_total * 100, 1) for producto in productos_paginados]}
        ]
    }
    return JsonResponse(datos, safe=False)


class RegistrarProducto(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/agregar_producto.html'
    success_url = reverse_lazy('listar_producto')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.ID_usuarioPropietario = self.request.user
        # Calcula el presupuesto total de los contratos seleccionados
        presupuesto_total = self.calcular_presupuesto_total(form)
        form.instance.presupuesto_total = presupuesto_total

        # Validación de Meta Actual y Valor Actual
        meta_actual = form.cleaned_data['Meta_Actual']
        valor_actual = form.cleaned_data['Valor_actual']
        if float(valor_actual) > float(meta_actual):
            form.add_error('Valor_actual', 'El valor actual no puede ser mayor que la meta actual.')
            return self.form_invalid(form)

        # Validación de contratos
        contratos = [
            form.cleaned_data['Contrato_1'],
            form.cleaned_data['Contrato_2'],
            form.cleaned_data['Contrato_3'],
            form.cleaned_data['Contrato_4'],
            form.cleaned_data['Contrato_5'],
        ]
        contratos_ids = [contrato.ID_Contrato for contrato in contratos if contrato]
        if len(contratos_ids) != len(set(contratos_ids)):
            form.add_error(None, 'No se puede seleccionar el mismo contrato en más de un campo.')
            return self.form_invalid(form)

        # Guardar archivos de soporte
        files = self.request.FILES.get('soporte')
        files_2 = self.request.FILES.get('soporte_2')
        permitidos = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/pdf']
        if files and files.content_type not in permitidos:
            form.add_error('soporte', 'Solo se permiten archivos Word, Excel y PDF')
            return self.form_invalid(form)
        if files_2 and files_2.content_type not in permitidos:
            form.add_error('soporte_2', 'Solo se permiten archivos Word, Excel y PDF')
            return self.form_invalid(form)

        if files:
            fs = FileSystemStorage()
            filename = self.generate_unique_filename(files.name, form.instance)
            fs.save(filename, files)
            form.instance.soporte = filename

        if files_2:
            fs = FileSystemStorage()
            filename_2 = self.generate_unique_filename(files_2.name, form.instance)
            fs.save(filename_2, files_2)
            form.instance.soporte_2 = filename_2

        # Actualizar el estado del producto según la vigencia
        vigencia_actual = datetime.now().year
        if int(form.instance.vigencia.Nombre) != vigencia_actual:
            form.instance.estado = 'Inactivo'
        else:
            form.instance.estado = 'Activo'

        # Guarda el formulario
        form.instance.save()  # Guarda la instancia del objeto
        producto = form.instance  # Obtiene la instancia del objeto guardada
    # Crear histórico de producto
        fecha_actual = datetime.now()
        HistoricoProducto.objects.create(
        ID_Producto=producto,
        Fecha=fecha_actual,
        Descripcion=f'Producto creado: {producto.Nombre_Producto}',
        ID_usuario=self.request.user,
        Tipo_cambio='Creación'
        )
        messages.success(self.request, 'Producto creado con éxito')
        return super().form_valid(form)

    def calcular_presupuesto_total(self, form):
        presupuesto_total = 0
        contratos = [
            form.cleaned_data['Contrato_1'],
            form.cleaned_data['Contrato_2'],
            form.cleaned_data['Contrato_3'],
            form.cleaned_data['Contrato_4'],
            form.cleaned_data['Contrato_5'],
        ]
        for contrato in contratos:
            if contrato:
                presupuesto_total += contrato.Valor
        return presupuesto_total

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contratos = Contrato.objects.all()
        contratos_json = []
        for contrato in contratos:
            contrato_json = {
                'id': contrato.ID_Contrato,
                'Valor': float(contrato.Valor),  # Convertir a float
            }
            contratos_json.append(contrato_json)
        context['contratos_json'] = json.dumps(contratos_json)
        return context

    def delete(self, *args, **kwargs):
        if self.object.soporte:
            archivo_path = f"media/{self.object.soporte}"
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
        self.object.delete(*args, **kwargs)

    def generate_unique_filename(self, filename, producto):
        nombre_archivo, extension = os.path.splitext(filename)
        fecha_carga = datetime.now().strftime("%Y%m%d")
        nuevo_nombre = f"{producto.Nombre_Producto}_{fecha_carga}{extension}"
        return nuevo_nombre


    
class ActualizarProducto(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/modificar_producto.html'
    success_url = reverse_lazy('listar_producto')
    success_message = 'Producto actualizado con éxito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contratos = Contrato.objects.all()
        contratos_json = []
        for contrato in contratos:
            contrato_json = {
                'id': contrato.ID_Contrato,
                'Valor': float(contrato.Valor),
            }
            contratos_json.append(contrato_json)
        context['contratos_json'] = json.dumps(contratos_json)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def calcular_presupuesto_total(self, form):
        presupuesto_total = 0
        contratos = [
            form.cleaned_data['Contrato_1'],
            form.cleaned_data['Contrato_2'],
            form.cleaned_data['Contrato_3'],
            form.cleaned_data['Contrato_4'],
            form.cleaned_data['Contrato_5'],
        ]
        contratoObj = json.loads(self.get_context_data()['contratos_json'])
        for contrato in contratos:
            if contrato:
                for contrato_json in contratoObj:
                    if contrato_json['id'] == contrato.ID_Contrato:
                        presupuesto_total += float(contrato_json['Valor'])
                        break
        return presupuesto_total
    def generate_unique_filename(self, filename, producto):
            nombre_archivo, extension = os.path.splitext(filename)
            fecha_carga = datetime.now().strftime("%Y%m%d")
            nuevo_nombre = f"{producto.Nombre_Producto}_{fecha_carga}{extension}"
            return nuevo_nombre
    def form_valid(self, form):
        # Calcula el presupuesto total de los contratos seleccionados
        presupuesto_total = self.calcular_presupuesto_total(form)
        form.instance.presupuesto_total = presupuesto_total

        # Validación de Meta Actual y Valor Actual
        meta_actual = form.cleaned_data['Meta_Actual']
        valor_actual = form.cleaned_data['Valor_actual']
        if float(valor_actual) > float(meta_actual):
            form.add_error('Valor_actual', 'El valor actual no puede ser mayor que la meta actual.')
            return self.form_invalid(form)

        # Validación de contratos
        contratos = [
            form.cleaned_data['Contrato_1'],
            form.cleaned_data['Contrato_2'],
            form.cleaned_data['Contrato_3'],
            form.cleaned_data['Contrato_4'],
            form.cleaned_data['Contrato_5'],
        ]
        contratos_ids = [contrato.ID_Contrato for contrato in contratos if contrato]
        if len(contratos_ids) != len(set(contratos_ids)):
            form.add_error(None, 'No se puede seleccionar el mismo contrato en más de un campo.')
            return self.form_invalid(form)

        # Guardar archivos de soporte
        files = self.request.FILES.get('soporte')
        files_2 = self.request.FILES.get('soporte_2')
        permitidos = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/pdf']
        if files and files.content_type not in permitidos:
            form.add_error('soporte', 'Solo se permiten archivos Word, Excel y PDF')
            return self.form_invalid(form)
        if files_2 and files_2.content_type not in permitidos:
            form.add_error('soporte_2', 'Solo se permiten archivos Word, Excel y PDF')
            return self.form_invalid(form)

        if files:
            fs = FileSystemStorage()
            filename = self.generate_unique_filename(files.name, form.instance)
            fs.save(filename, files)
            form.instance.soporte = filename

        if files_2:
            fs = FileSystemStorage()
            filename_2 = self.generate_unique_filename(files_2.name, form.instance)
            fs.save(filename_2, files_2)
            form.instance.soporte_2 = filename_2

        # Actualizar el estado del producto según la vigencia
        vigencia_actual = datetime.now().year
        if int(form.instance.vigencia.Nombre) != vigencia_actual:
            form.instance.estado = 'Inactivo'
        else:
            form.instance.estado = 'Activo'


        # Crear histórico de producto
        fecha_actual = datetime.now()
        HistoricoProducto.objects.create(
            ID_Producto=form.instance,
            Fecha=fecha_actual,
            Descripcion=f'Producto actualizado: {form.instance.Nombre_Producto}',
            ID_usuario=self.request.user,
            Tipo_cambio='Actualización'
        )

        messages.success(self.request, 'Producto actualizado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))




def descargar_archivo(request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        archivo = producto.soporte
        ruta_archivo = f'media/{archivo}'
        
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'rb') as archivo_descargar:
                respuesta = HttpResponse(archivo_descargar.read(), content_type='application/octet-stream')
                respuesta['Content-Disposition'] = f'attachment; filename="{archivo}"'
                return respuesta
        else:
            return HttpResponseNotFound(f'El archivo {archivo} no existe')
def descargar_archivo_soporte_2(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    archivo = producto.soporte_2
    if not archivo:
        return HttpResponseNotFound('No hay archivo asociado')
    ruta_archivo = f'media/{archivo}'
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'rb') as archivo_descargar:
            respuesta = HttpResponse(archivo_descargar.read(), content_type='application/octet-stream')
            respuesta['Content-Disposition'] = f'attachment; filename="{archivo}"'
            return respuesta
    else:
        return HttpResponseNotFound(f'El archivo {archivo} no existe')


        
class EliminarProducto(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('listar_producto')
    template_name = 'producto/eliminar_producto.html'  
    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        producto.estado = 'Inhabilitado'
        producto.save()
        fecha_actual = datetime.now()
        HistoricoProducto.objects.create(
            ID_Producto=producto,
            Fecha=fecha_actual,
            Descripcion=f'Producto eliminado: {producto.Nombre_Producto}',
            ID_usuario=request.user,
            Tipo_cambio='Eliminación'
        )
        return redirect('listar_producto')

def reprogramar_vigencia(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReprogramarVigenciaForm(request.POST, instance=producto)
        if form.is_valid():
            # Obtener el valor de la vigencia actual
            vigencia_anterior = producto.vigencia
            # Asignar el nuevo valor de vigencia
            producto.vigencia = form.cleaned_data['vigencia']
            # Asignar el valor de la vigencia anterior
            producto.vigencia_anterior = vigencia_anterior
            # Verificar si el campo vigencia ha cambiado
            if producto.vigencia.id != vigencia_anterior.id:
                # Verificar las fechas inicial y final de la vigencia
                fecha_actual = datetime.date.today()
                anio_actual = fecha_actual.year
                fecha_inicial = producto.vigencia.fecha_inicial
                fecha_final = producto.vigencia.fecha_final
                if fecha_inicial > datetime.date(anio_actual, 12, 31) or fecha_final < datetime.date(anio_actual, 1, 1):
                    producto.estado = 'Inactivo'
                else:
                    producto.estado = 'Activo_Reprogramado'
            else:
                producto.estado = 'Activo_Reprogramado'
            producto.save()
            HistoricoProducto.objects.create(
                ID_Producto=producto,
                Fecha=datetime.now(),
                Descripcion=f'Vigencia reprogramada: {producto.Nombre_Producto}',
                ID_usuario=request.user,
                Tipo_cambio='Reprogramación'
            )
            messages.success(request, 'Vigencia reprogramada con éxito')
            return redirect('listar_producto')
    else:
        form = ReprogramarVigenciaForm(instance=producto)
    return render(request, 'producto/reprogramar_vigencia.html', {'form': form})
#Historial

class historico_producto(LoginRequiredMixin,ListView):
    model = HistoricoProducto
    template_name = 'producto/Historial.html'

    def get_queryset(self):
        return self.model.objects.all()



        
#CRUD INDICADOR-PRODUCTO

class ListadoIndicadorProducto(LoginRequiredMixin, ListView):
    model = Indicador_Producto
    template_name = 'indicador_producto/listar_indicador_producto.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class RegistrarIndicadorProducto(LoginRequiredMixin, CreateView):
    model = Indicador_Producto
    form_class = IndicadorProductoForm
    template_name = 'indicador_producto/agregar_indicador_producto.html'
    success_url = reverse_lazy('listar_indicador_producto')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Indicador de producto creado con éxito')
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)
        
class ActualizarIndicadorProducto(LoginRequiredMixin, UpdateView):
    model = Indicador_Producto
    form_class = IndicadorProductoForm
    template_name = 'indicador_producto/modificar_indicador_producto.html'
    success_url = reverse_lazy('listar_indicador_producto')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Indicador de producto actualizado con éxito')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class EliminarIndicadorProducto(LoginRequiredMixin, DeleteView):
    model = Indicador_Producto
    template_name = 'indicador_producto/eliminar_indicador_producto.html'
    success_url = reverse_lazy('listar_indicador_producto')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tiene_dependencias():
            messages.error(request, 'No se puede eliminar este indicador de producto porque tiene dependencias con productos.')
            return redirect('listar_indicador_producto')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.add_message(self.request, messages.SUCCESS, 'Indicador de producto eliminado con éxito')
        return response
