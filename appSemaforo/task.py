from django_q.tasks import async_task
from django.utils import timezone
from .models import Producto, Vigencia

@async_task
def verificar_vigencia_productos():
    vigencias = Vigencia.objects.all()
    for vigencia in vigencias:
        if vigencia.fecha_final <= timezone.now():
            productos = Producto.objects.filter(vigencia=vigencia)
            for producto in productos:
                if producto.estado == 'Activo':
                    producto.estado = 'Expirada'
               
                else:
                    producto.estado = 'Inactivo'
                producto.save()

Q_CLUSTER_SCHEDULE = [
    {
        'func': 'appSemaforo.tasks.verificar_vigencia_productos',
        'args': [],
        'kwargs': {},
        'schedule': '0 0 * * *',  # ejecuta la tarea cada día a las 00:00
    },
]