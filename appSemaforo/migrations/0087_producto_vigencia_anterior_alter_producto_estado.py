# Generated by Django 5.1 on 2025-01-17 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0086_remove_producto_nueva_vigencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='vigencia_anterior',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vigenciaAnterior', to='appSemaforo.vigencia'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('Activo', 'ACTIVO'), ('Activo_Reprogramado', 'ACTIVO_REPROGRAMADO'), ('Inactivo', 'INACTIVO'), ('Inhabilitado', 'INHABILITADO'), ('Expirada', 'EXPIRADA')], max_length=50),
        ),
    ]
