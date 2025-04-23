from celery import shared_task
from .models import Producto

@shared_task
def actualizar_estados_productos():
    productos = Producto.objects.all()
    vigencia_actual = datetime.now().year
    for producto in productos:
        if producto.vigencia != vigencia_actual:
            producto.estado = False
        else:
            producto.estado = True
        producto.save()