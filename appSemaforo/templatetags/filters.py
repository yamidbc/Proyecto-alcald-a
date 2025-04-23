from django import template
from decimal import Decimal, ROUND_HALF_UP
import decimal
register = template.Library()

@register.filter
def dividir(value, arg):
    return (value / arg)

@register.filter
def multiply(value, arg):
    return value * arg



@register.simple_tag
def calcular_porcentaje(valor, total):
    print(f"Valor: {valor}, Total: {total}")
    try:
        valor = Decimal(valor)
        total = Decimal(total)
    except decimal.InvalidOperation:
        return "0.0"
    
    if total == 0:
        return "0.0"
    
    porcentaje = (valor / total) * 100
    print(f"Porcentaje: {porcentaje}")
    return Decimal(porcentaje).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

@register.filter
def calificar(producto):
    progreso_porcentaje = producto.Valor_actual / producto.Meta_Actual * 100
    presupuesto_porcentaje = producto.Presupuesto_utilizado / producto.presupuesto_total * 100
    if progreso_porcentaje == 100:
        if presupuesto_porcentaje < 55:
            return 'Bajo'
        elif 55 <= presupuesto_porcentaje < 70:
            return 'Medio'
        else:
            return 'Alto'
    else:
        return 'No-aplica'
    


@register.filter
def parpadeo(color):
    print(f"Color: {color}")
    if color == "verde":
        return ""
    elif color == "amarillo":
        return "parpadeo-medio"
    elif color == "rojo":
        return "parpadeo-rapido"
    return ""