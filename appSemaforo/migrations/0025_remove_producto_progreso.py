# Generated by Django 5.1 on 2024-09-17 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0024_producto_valor_actual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='Progreso',
        ),
    ]
