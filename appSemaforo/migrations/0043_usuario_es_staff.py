# Generated by Django 5.1 on 2024-10-28 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0042_producto_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='es_staff',
            field=models.BooleanField(default=False),
        ),
    ]
