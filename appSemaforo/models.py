from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
import enum
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q

# Crear los modelos aqui



class UsuarioManager(BaseUserManager):

    def create_user(self,email,username,Nombre,Apellidos,Telefono, password=None):
        if not email:
            raise ValueError('el usuario debe tener un correo electrónico!')

        usuario = self.model(username=username,
                             email = self.normalize_email(email),
                             Nombre=Nombre,
                             Apellidos=Apellidos,
                             Telefono=Telefono,
                             )
        usuario.set_password(password)
        usuario.save()
        return usuario
    def create_superuser(self,email,username,Nombre,Apellidos,Telefono,password):
        usuario = self.create_user(
                            email,
                            username=username,
                            Nombre=Nombre,
                            Apellidos=Apellidos,
                            Telefono=Telefono,
                            password=password)
        usuario.is_superuser = True
        usuario.save()
        return usuario
class Cargo_usuario(models.Model):
    ID_cargo= models.IntegerField(primary_key=True)
    nombre= models.CharField(max_length=150)

    def __str__(self):
        return f'{self.nombre}'
    class Meta:
        db_table = 'cargo_usuario'
   
class Usuario(AbstractBaseUser):
    username=models.CharField(max_length=50, unique=True)
    email=models.CharField(max_length=150, unique=True, null=True)
    password=models.CharField(max_length=255)
    Telefono=models.BigIntegerField(null=True)
    Nombre=models.CharField(max_length=100, null=True)
    Apellidos=models.CharField(max_length=150, null=True)
    
    usuario_activo=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_guest=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    Cargo_usuario= models.ForeignKey(Cargo_usuario, on_delete=models.CASCADE )
    objects=UsuarioManager()
    
    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS=['email','Nombre','Apellidos','Telefono']
    
    def tiene_dependencias(self):
        return Producto.objects.filter(usuario=self).exists()
    
    def __str__(self):
        return f'{self.Nombre} {self.Apellidos}'
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self, app_alcaldia):
        return True  
    @property
    def is_staff(self):
        return self.is_superuser
    
    class Meta:
        db_table = 'usuario'
        
# Modelos generados realativamente con la conexión a BD MYSQL
   
class Linea_estrategica(models.Model):
    Nombre= models.CharField(max_length=150)
    Cod_LineaEstrategica = models.CharField(max_length=10)
    
    def tiene_dependencias(self):
        # Verifica si la línea estratégica tiene dependencias con pilares sectoriales
        return self.pilar_sectorial_set.exists()
    def __str__(self):
        return f' {self.Nombre}'
    class Meta:
        db_table = 'linea_estrategica'
        
class Pilar_sectorial(models.Model):
    CodigoP= models.IntegerField(primary_key=True, unique=True)
    Nombre_Pilar= models.CharField(max_length=100)
    Linea_estrategica = models.ForeignKey(Linea_estrategica, on_delete=models.PROTECT, null=True, blank=True)
    
    def tiene_dependencias(self):
        # Verifica si la línea estratégica tiene dependencias con programa
        return self.programa_set.exists()
    
    def __str__(self):
        return f' {self.Nombre_Pilar}'
    class Meta:
        db_table = 'pilar_sectorial'
        

class Programa (models.Model):
    Cod_programa = models.IntegerField(null=True)
    Nombre_Programa = models.CharField(max_length=350)
    
    pilar_sectorial = models.ForeignKey(Pilar_sectorial, on_delete=models.PROTECT, null=True, blank=True)
    
    def tiene_dependencias(self):
        # Verifica si la línea estratégica tiene dependencias con programa
        return self.producto_set.exists()
    
    def __str__(self):
        return f'{self.Nombre_Programa}'
    class Meta:
        db_table = 'programa'



class Indicador_Producto(models.Model):
    
    Codigo_indicador = models.IntegerField(null=False,blank=False)
    Nombre= models.CharField(max_length=200)

    def tiene_dependencias(self):
        return Producto.objects.filter(ID_Indicador=self).exists()

    def __str__(self):
        return f'{self.Nombre}'
    class Meta:
        db_table = 'indicador_producto'
        
class Vigencia(models.Model):
    Nombre = models.CharField(max_length=255)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()

    def __str__(self):
        return f'{self.Nombre}'
    class Meta:
        db_table = 'vigencia'       

class Contrato(models.Model):
    ID_Contrato =models.IntegerField(primary_key=True, null=False, blank=False)
    Duración = models.CharField(max_length=150)
    Objeto = models.CharField(max_length=255)
    Numero_beneficiarios=models.IntegerField()
    Valor=models.DecimalField( max_digits=10, decimal_places=2)
    
    def tiene_dependencias(self):
        return Producto.objects.filter(
            Q(Contrato_1=self) | Q(Contrato_2=self) | Q(Contrato_3=self) | Q(Contrato_4=self) | Q(Contrato_5=self)
        ).exists()
    
    def __str__(self):
        return f'{self.ID_Contrato}'
    class Meta:
        db_table = 'contrato'      

class EstadoChoices(enum.Enum):
    ACTIVO = 'Activo'
    ACTIVO_REPROGRAMADO ='Activo_Reprogramado' 
    INACTIVO = 'Inactivo'
    INHABILITADO = 'Inhabilitado'
    EXPIRADA = 'Expirada'

PRIORITY_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]    
MEDICION_CHOICES = [
('','Seleccione una opción'),
('HÉCTAREAS','Héctareas'),
('KILÓMETROS','Kilómetros'),
('METROS CUADRADOS','Metros Cuadrados'),
('METROS LINEALES','Metros Lineales'),
('MINUTOS','Minutos'),
('NÚMERO','Número'),
    ] 
          
class Producto(models.Model):
    
    Nombre_Producto =models.CharField(max_length=200)
    Codigo_producto= models.IntegerField(unique=True)
    Valor_actual = models.DecimalField(max_digits=10, decimal_places=2)
    Descripción = models.TextField()
    Medición = models.CharField(max_length=150)
    Unidad_de_medida = models.CharField(max_length=50,choices=MEDICION_CHOICES)
    Linea_base = models.DecimalField(max_digits=17,decimal_places=2)
    Meta_Actual = models.DecimalField(max_digits=10,decimal_places=2)
    soporte = models.CharField( max_length=250, blank=True, null=True)
    soporte_2 = models.CharField( max_length=250, blank=True, null=True)
    ID_usuarioPropietario = models.ForeignKey(Usuario,on_delete=models.PROTECT, null=False, blank= False, related_name='AsignarProducto')
    ID_usuarioAsignado = models.ForeignKey(Usuario,on_delete=models.PROTECT, null=False, blank= False, related_name='AsignadoProducto')
    vigencia = models.ForeignKey(Vigencia, on_delete=models.PROTECT)
    
    vigencia_anterior = models.ForeignKey(Vigencia, on_delete=models.PROTECT, null=True, blank=True,related_name='vigenciaAnterior')
    estado = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in EstadoChoices])
    Prioridad = models.CharField(max_length=5,choices=PRIORITY_CHOICES,default='MEDIA',blank=False,null=False)
    ID_programa = models.ForeignKey(Programa,on_delete=models.PROTECT, null=False, blank= False)
    ID_Pilar_Sectorial = models.ForeignKey(Pilar_sectorial,on_delete=models.PROTECT, null=False, blank= False)
    ID_LineaEstrategica = models.ForeignKey(Linea_estrategica,on_delete=models.PROTECT, null=False, blank= False)
    Secretario_responsable= models.ForeignKey(Cargo_usuario, on_delete=models.PROTECT,null=False, blank= False)
    ID_Indicador = models.ForeignKey(Indicador_Producto,on_delete=models.PROTECT, null=False, blank= False)
    fecha_creacion = models.DateField(auto_now_add=True)
    Contrato_1 = models.ForeignKey(Contrato,on_delete=models.CASCADE, related_name=('ContratoUno'))
    Contrato_2 = models.ForeignKey(Contrato,on_delete=models.CASCADE, related_name=('ContratoDos'))
    Contrato_3 = models.ForeignKey(Contrato,on_delete=models.CASCADE, related_name=('ContratoTres'))
    Contrato_4 = models.ForeignKey(Contrato,on_delete=models.CASCADE, related_name=('ContratoCuatro'))
    Contrato_5 = models.ForeignKey(Contrato,on_delete=models.CASCADE, related_name=('ContratoCinco'))
    Presupuesto_utilizado = models.DecimalField(max_digits=10, decimal_places=2)
    presupuesto_total=models.DecimalField( max_digits=10, decimal_places=2)
    
    def calcular_presupuesto_total(self):
        presupuesto_total = 0
        contratos = [self.Contrato_1, self.Contrato_2, self.Contrato_3, self.Contrato_4, self.Contrato_5]
        for contrato in contratos:
            if contrato is not None:
                presupuesto_total += contrato.Valor
        return presupuesto_total

#meses vigencia------------

    @property
    def meses(self):
        meses = []
        for mes in range(1, 13):
            fecha = datetime(self.vigencia, mes, 1)
            meses.append(fecha)
        return meses

    @property
    def color_semaforo(self):
        progreso_porcentaje = self.Presupuesto_utilizado / self.presupuesto_total * 100
        if progreso_porcentaje < 55:
            return "rojo"
        elif 55 <= progreso_porcentaje < 70:
            return "amarillo"
        else:
            return "verde"



 # ------------meta progreso------
    @property
    def status_progreso(self):
        progreso = (self.Valor_actual / self.Meta_Actual) * 100
        if progreso > 0 and progreso <= 10:
            return 'Iniciada'
        elif progreso > 10 and progreso < 100:
            return 'En progreso'
        elif progreso == 100:
            return 'Completada'
        else:
            return 'No iniciada'
    
    def __str__(self):
        return f' {self.Nombre_Producto}'
    class Meta:
        db_table = 'producto'

   #---calificaciones
    @property
    def calcular_calificacion(self):
        progreso_porcentaje = self.Valor_actual / self.Meta_Actual * 100
        presupuesto_porcentaje = self.Presupuesto_utilizado / self.presupuesto_total * 100
        
        if progreso_porcentaje == 100:
            if presupuesto_porcentaje < 55:
                return 'Bajo'
            elif 55 <= presupuesto_porcentaje < 70:
                return 'Medio'
            else:
                return 'Alto'
        else:
            return 'No aplica' 


        
class HistoricoProducto(models.Model):
    
    Fecha = models.DateTimeField()
    ID_Producto =models.ForeignKey(Producto,on_delete=models.SET_NULL, null=True, blank= True)
    ID_usuario =  models.ForeignKey(Usuario,on_delete=models.CASCADE, null=True, blank= True)
    Tipo_cambio = models.CharField(max_length=50)  # Agregamos un campo para el tipo de cambio
    Descripcion= models.CharField(max_length=255)

    def __str__(self):
        return f'{self.ID}, {self.Fecha},{self.Soporte},{self.ID_Producto},{self.ID_usuario}'
    class Meta:
        db_table = 'historico_producto'    
    