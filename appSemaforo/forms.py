from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import FileInput
from appSemaforo.models import Usuario,Linea_estrategica,Pilar_sectorial,Programa,Producto,Indicador_Producto,Vigencia,Cargo_usuario,Indicador_Producto,Contrato
from .models import EstadoChoices

class FormularioLogin(forms.Form):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                usuario = Usuario.objects.get(username=username)
                if not usuario.check_password(password):
                    self.add_error('password', 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                self.add_error('username', 'Usuario no encontrado')
        else:
            self.add_error('username', 'Debe completar todos los campos')

        return cleaned_data
    
class FormularioUsuarioPublico(forms.ModelForm):
    password = forms.CharField(label='contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese su contraseña', 'id': 'password', 'required': 'required', }))
    password1 = forms.CharField(label='contraseña de confirmación', widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese nuevamente su contraseña', 'id': 'password1', 'required': 'required', }))
    Cargo_usuario = forms.ModelChoiceField(queryset=Cargo_usuario.objects.all(), label="Cargo Usuario", empty_label="Seleccione un cargo", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'Nombre', 'Apellidos', 'Telefono','Cargo_usuario')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese su correo electrónico', }),
            'Nombre': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese su nombre', }),
            'Apellidos': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese sus apellidos', }),
            'username': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese su nombre de usuario', }),
            'Telefono': forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Ingrese su teléfono', }),
            'Cargo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }    
class FormularioUsuario(forms.ModelForm):

  password = forms.CharField(label='contraseña', widget= forms.PasswordInput(
    attrs={
        'class' : 'form-control col-7',
        'placeholder' : 'Ingrese su contraseña',
        'id' : 'password',
        'required' : 'required',
          
      }
    ))
  password1= forms.CharField(label='contraseña de confirmación', widget=forms.PasswordInput(
      attrs={
        'class' : 'form-control col-7',
        'placeholder' : 'Ingrese nuevamente su contraseña',
        'id' : 'password1',
        'required' : 'required',      
      }
  ))
  
  is_superuser = forms.BooleanField(label='Superusuario', required=False)
  is_guest = forms.BooleanField(label='Usuario Invitado', required=False)
  
  
  class Meta :
      model = Usuario
      fields = ('email','username','Nombre','Apellidos', 'Telefono', 'is_superuser','is_guest','Cargo_usuario')
      widgets = {
          'email': forms.EmailInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese su correo eléctronico, ejmplo pepito@dominio.com.co: ',
                
              }
          ),
          'Nombre': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese su nombre',
              }
          ),
          'Apellidos': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese sus apellidos',
              }
          ), 
          'username': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese su nombre de usuario',
              }
          ), 
          'Telefono': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese su telefono',
              }
          ), 

         'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
         'is_guest': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        'Cargo_usuario':forms.Select(attrs={'class': 'form-control col-7'
                                                      
                                                      }),
          
      }
  Cargo_usuario = forms.ModelChoiceField(queryset=Cargo_usuario.objects.all(), label="Cargo Usuario", empty_label="Seleccione un cargo",widget=forms.Select(attrs={'class': 'form-control col-7'}),)
    
    
  def __init__(self, *args, **kwargs):
    super(FormularioUsuario, self).__init__(*args, **kwargs)
    self.fields['Cargo_usuario'].queryset = Cargo_usuario.objects.all()
      
def clean_password1(self):
    """"Validación de contraseña
    valida la contaraseña antes de ser encriptada en el registro

    Exepciones:
     -validationError:--validación de contraseñas iguales 
    """""
    password = self.cleaned_data.get('password')
    password1 = self.cleaned_data.get('password1')
    if password != password1 :
        raise forms.ValidationError('Las contraseñas no coinciden!')
    return password1
def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])
    if commit:
        user.save()
        return user
    




        
class FormularioLineaE(forms.ModelForm):
    
    class Meta:
        model = Linea_estrategica
        fields = ('Cod_LineaEstrategica','Nombre')
        widgets = {
            'Cod_LineaEstrategica': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el codigo de la linea estrategica',
              }
          ), 
            'Nombre': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el nombre de la linea estrategica ',
                
              }
          ),
            
            
          
      }
        
class FormularioContrato(forms.ModelForm):
    
    class Meta:
        model = Contrato
        fields = ('ID_Contrato','Objeto','Duración','Numero_beneficiarios', 'Valor')
        widgets = {
            'ID_Contrato': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el codigo del contrato',
              }
          ), 
            'Objeto': forms.Textarea(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el objeto del contrato',
              }
          ), 
            'Duración': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese la duración del contrato',
              }
          ), 
            'Numero_beneficiarios': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el número de beneficiarios ',
                
              }
          ),
            'Valor': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el valor del contrato ',
                
              }
          ),      
      }
    
class FormularioPilarS(forms.ModelForm):
    CodigoP =forms.IntegerField(label='Código Pilar',widget=forms.NumberInput(attrs={'class': 'form-control col-7', 'placeholder' : 'Ingrese código para el pilar sectorial'}))
    class Meta:
        model = Pilar_sectorial
        fields = ('CodigoP','Nombre_Pilar','Linea_estrategica')
        widgets = {
            'CodigoP': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el codigo para el pilar sectorial',
              }
          ), 
            'Nombre_Pilar': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el nombre para el pilar sectorial ',
                
              }
          ),
            'Linea_estrategica': forms.Select(attrs={'class': 'form-control col-7'
                                                      
                                                      }),


      }
    
    
    Linea_estrategica = forms.ModelChoiceField(queryset=Linea_estrategica.objects.all(), label="Linea estrategica", empty_label="Seleccione un Linea",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    
    
    def __init__(self, *args, **kwargs):
        super(FormularioPilarS, self).__init__(*args, **kwargs)
        self.fields['Linea_estrategica'].queryset = Linea_estrategica.objects.all()
        
class FormularioPrograma(forms.ModelForm):
    Cod_programa = forms.IntegerField(label='Codigo programa', widget=forms.NumberInput(attrs={'class':'form-control col-7', 'placeholder': 'Ingrese el codigo del programa',}))
    class Meta:
        model = Programa
        fields = ('Cod_programa','Nombre_Programa','pilar_sectorial')
        widgets = {
            'Nombre_Programa': forms.TextInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el nombre del programa',
              }
          ), 
           
           
            'Cod_programa': forms.NumberInput(
              attrs={
                  'class' : 'form-control col-7',
                  'placeholder': 'Ingrese el codigo del programa',
                
              }
          ),
           
           'pilar_sectorial': forms.Select(attrs={'class': 'form-control col-7'
                                                      
                                                      }),

      }
        
    pilar_sectorial = forms.ModelChoiceField(queryset=Pilar_sectorial.objects.all(), label="Pilar Sectorial", empty_label="Seleccione un pilar", widget=forms.Select(attrs={'class': 'form-control col-7'}))
    
    
    def __init__(self, *args, **kwargs):
        super(FormularioPrograma, self).__init__(*args, **kwargs)
        self.fields['pilar_sectorial'].queryset = Pilar_sectorial.objects.all()
        
        
        
        
        
        
#formulario producto
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
class ProductoForm(forms.ModelForm):
    soporte = forms.FileField(widget=forms.FileInput(attrs={'class': '',
                                                            'accept': '.doc, .docx, .xls, .xlsx, .pdf' }),required=False)
    soporte_2 = forms.FileField(widget=forms.FileInput(attrs={'class': '',
                                                            'accept': '.doc, .docx, .xls, .xlsx, .pdf' }),required=False)

    
    
    estado = forms.ChoiceField(label='Estado', choices=[(tag.value, tag.name) for tag in EstadoChoices], widget=forms.HiddenInput(attrs={'disabled': True}), required=False)
    Nombre_Producto=forms.CharField(label='Nombre Meta',widget=forms.TextInput(attrs={'class': 'form-control col-7', 'placeholder' : 'Ingrese el nombre de la meta (Obligatorio)'}))
    
    estado_hidden = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )# Asigna el valor inicial del campo deshabilitado
    Prioridad = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        initial='MEDIA',
        widget=forms.Select(attrs={'class': 'form-control col-7'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        vigencia = cleaned_data.get('vigencia')
       
    def delete(self, *args, **kwargs):
        if self.instance.soporte:
            archivo_path = f"media/{self.instance.soporte}"
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
        self.instance.delete(*args, **kwargs)

    
    class Meta:
        model = Producto
        fields = ('Codigo_producto','Nombre_Producto','Meta_Actual','Valor_actual','Medición','Unidad_de_medida','ID_Indicador','Descripción','Linea_base','ID_LineaEstrategica','Secretario_responsable', 'ID_Pilar_Sectorial','ID_programa','ID_usuarioPropietario','ID_usuarioAsignado','vigencia','estado','Prioridad','estado_hidden','soporte','soporte_2','Contrato_1','Contrato_2','Contrato_3','Contrato_4','Contrato_5','Presupuesto_utilizado', 'presupuesto_total')
        initial={'Unidad_de_medida':'',}
        widgets = {
            
            'Codigo_producto': forms.TextInput(attrs={'class': 'form-control col-7',
                                                      'placeholder' : 'Ingrese el codigo para la meta (Obligatorio)' 
                                                      }),
            'Nombre_Producto': forms.TextInput(attrs={'class': 'form-control col-7',
                                                      'placeholder' : 'Ingrese el nombre de la meta (Obligatorio)'
                                                      
                                                      }),
            'Meta_Actual': forms.NumberInput(attrs={'class': 'form-control col-7',
                                                  'placeholder' : 'Ingrese valor de la meta actual a cumplir (Obligatorio)'
                                                  }),
            
            'Valor_actual': forms.NumberInput(attrs={'class':'form-control col-7',
                                                     'placeholder' : 'Ingrese el valor de avance de la meta actual (Obligatorio)'
                                                     }), 
            'Medición': forms.TextInput(attrs={'class': 'form-control col-7',
                                               'placeholder' : 'Ingrese el valor de medición para la meta (Obligatorio)'
                                               }),
            'Unidad_de_medida': forms.Select(attrs={'class': 'form-control col-7'
                                                       
                                                       }),
            'ID_Indicador': forms.Select(attrs={'class': 'form-control col-7'
                                                
                                                }),
            
            'Descripción': forms.Textarea(attrs={'class': 'form-control col-7',
                                                 
                                                 
                                                 }),
            'Linea_base': forms.NumberInput(attrs={'class': 'form-control col-7',
                                                   'placeholder' : 'Ingrese meta lograda en el anterior cuatrienio anterior (Obligatorio)'
                                                   }),
             'ID_LineaEstrategica': forms.Select(attrs={'class': 'form-control col-7'
                                                       
                                                       }),
            'Secretario_responsable': forms.Select(attrs={'class': 'form-control col-7'
                                                       
                                                       }),
            'ID_Pilar_Sectorial': forms.Select(attrs={'class': 'form-control col-7'
                                                      
                                                      }),
            'ID_programa': forms.Select(attrs={'class': 'form-control col-7'
                                               
                                               }),

            'ID_usuarioPropietario': forms.Select(attrs={'class': 'form-control col-7'
                                                         
                                                         }),
            'ID_usuarioAsignado': forms.Select(attrs={'class': 'form-control col-7'
                                                      
                                                      }),
            'vigencia': forms.Select(attrs={'class': 'form-control col-3'}), 
            
            'estado': forms.Select(attrs={'class': 'form-control col-7',
                                          
                                           }),
            'Prioridad': forms.Select(attrs={'class': 'form-control col-7',
                                          
                                           }),
            'Contrato_1': forms.Select(attrs={'class': 'form-control col-7'
                                                                    
                                                                    }),
            'Contrato_2': forms.Select(attrs={'class': 'form-control col-7'
                                                                    
                                                                    }),
            'Contrato_3': forms.Select(attrs={'class': 'form-control col-7'
                                                                    
                                                                    }),
            'Contrato_4': forms.Select(attrs={'class': 'form-control col-7'
                                                                    
                                                                    }),
            'Contrato_5': forms.Select(attrs={'class': 'form-control col-7'
                                                                    
                                                                    }),            
            
            'soporte':forms.FileInput(attrs={'class': 'dropzone dz-clickable','required':False
                                             
                                                      }),
            'soporte_2':forms.FileInput(attrs={'class': 'dropzone dz-clickable','required':False
                                             
                                                      }),
            'Presupuesto_utilizado': forms.NumberInput(attrs={'class': 'form-control col-7',
                                                  'placeholder' : 'Ingrese valor de presupuesto utilizado (Obligatorio)'
                                                  }),
            
            
            'presupuesto_total': forms.NumberInput(attrs={'class': 'form-control col-7',
                                                  
                                                  }),
            
        }

    ID_usuarioPropietario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Usuario Propietario",
        empty_label="Seleccione un usuario",
        widget=forms.HiddenInput(),
        required=False
    )
    ID_usuarioAsignado = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Usuario Asignado*", empty_label="Seleccione un usuario",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    Secretario_responsable=forms.ModelChoiceField(queryset=Cargo_usuario.objects.all(), label="Secretaria responsable*", empty_label="Seleccione uno",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    ID_programa = forms.ModelChoiceField(queryset=Programa.objects.all(), label="Programa*", empty_label="Seleccione un programa",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    ID_Pilar_Sectorial = forms.ModelChoiceField(queryset=Pilar_sectorial.objects.all(), label="Pilar Sectorial*", empty_label="Seleccione un pilar",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    ID_LineaEstrategica = forms.ModelChoiceField(queryset=Linea_estrategica.objects.all(), label="Línea Estratégica*", empty_label="Seleccione una línea",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    ID_Indicador = forms.ModelChoiceField(queryset=Indicador_Producto.objects.all(), label="Indicador*", empty_label="Seleccione un indicador", widget=forms.Select(attrs={'class': 'form-control col-7'}),)
    
    
    vigencia = forms.ModelChoiceField(queryset=Vigencia.objects.all(), label="Vigencia Meta*", empty_label="Seleccione una vigencia",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    Contrato_1 = forms.ModelChoiceField(queryset=Contrato.objects.all(), label="Contrato 1*", empty_label="Seleccione un contrato",widget=forms.Select(attrs={'class': 'form-control col-7'}))
    Contrato_2 = forms.ModelChoiceField(queryset=Contrato.objects.all(), label="Contrato 2", empty_label="Seleccione un contrato",widget=forms.Select(attrs={'class': 'form-control col-7'}), required=False)
    Contrato_3 = forms.ModelChoiceField(queryset=Contrato.objects.all(), label="Contrato 3", empty_label="Seleccione un contrato",widget=forms.Select(attrs={'class': 'form-control col-7'}), required=False)
    Contrato_4 = forms.ModelChoiceField(queryset=Contrato.objects.all(), label="Contrato 4", empty_label="Seleccione un contrato",widget=forms.Select(attrs={'class': 'form-control col-7'}), required=False)
    Contrato_5 = forms.ModelChoiceField(queryset=Contrato.objects.all(), label="Contrato 5", empty_label="Seleccione un contrato",widget=forms.Select(attrs={'class': 'form-control col-7'}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['ID_usuarioPropietario'].queryset = Usuario.objects.all()
        self.fields['ID_usuarioAsignado'].queryset = Usuario.objects.all()
        self.fields['vigencia'].queryset = Vigencia.objects.all()
        self.fields['ID_programa'].queryset = Programa.objects.all()
        self.fields['ID_Pilar_Sectorial'].queryset = Pilar_sectorial.objects.all()
        self.fields['ID_LineaEstrategica'].queryset = Linea_estrategica.objects.all()
        self.fields['Secretario_responsable'].queryset = Cargo_usuario.objects.all()
        self.fields['ID_Indicador'].queryset = Indicador_Producto.objects.all()
        self.fields['estado_hidden'].initial = self.fields['estado'].initial
        self.fields['Contrato_1'].queryset = Contrato.objects.all()
        self.fields['Contrato_2'].queryset = Contrato.objects.all()
        self.fields['Contrato_3'].queryset = Contrato.objects.all()
        self.fields['Contrato_4'].queryset = Contrato.objects.all()
        self.fields['Contrato_5'].queryset = Contrato.objects.all()
        self.fields['ID_usuarioPropietario'].initial = self.request.user
        
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.id:  # Verifica si se está actualizando un producto
            soporte = cleaned_data.get('soporte')
            soporte_2 = cleaned_data.get('soporte_2')
            if not soporte and not soporte_2:  # Verifica si ambos campos están vacíos
                self.add_error('soporte', 'Es necesario agregar un soporte para justificar la actualización.')
                self.add_error('soporte_2', 'Es necesario agregar un soporte para justificar la actualización.')
        return cleaned_data




class ReprogramarVigenciaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('vigencia',)

#Formulario para CRUD indicador producto
class IndicadorProductoForm(forms.ModelForm):
    class Meta:
        model = Indicador_Producto
        fields = ('Codigo_indicador','Nombre' )
        labels = {
            'Codigo_indicador': 'Codigo del indicador de producto',
            'Nombre': 'Nombre del indicador de producto',
            
        }
        widgets = {
            'Codigo_indicador': forms.NumberInput(attrs={'class': 'form-control col-4'}),
            'Nombre': forms.TextInput(attrs={'class': 'form-control col-4'}),
        }