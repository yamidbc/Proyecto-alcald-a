# Generated by Django 5.1 on 2024-11-27 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0080_remove_producto_prioridad_remove_producto_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='fecha_actualizacion',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='fecha_eliminacion',
        ),
    ]
