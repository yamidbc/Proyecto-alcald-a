# Generated by Django 5.1 on 2024-11-14 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0069_remove_linea_estrategica_secretario_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Secretario_responsable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appSemaforo.cargo_usuario'),
            preserve_default=False,
        ),
    ]
