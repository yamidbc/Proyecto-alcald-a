# Generated by Django 5.1 on 2025-01-16 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0085_producto_nueva_vigencia_usuario_is_guest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='nueva_vigencia',
        ),
    ]
