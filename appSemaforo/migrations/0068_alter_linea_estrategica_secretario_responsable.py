# Generated by Django 5.1 on 2024-11-14 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0067_remove_cargo_usuario_id_cargo_usuario_id_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linea_estrategica',
            name='Secretario_Responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appSemaforo.cargo_usuario'),
        ),
    ]
