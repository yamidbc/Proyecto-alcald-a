# Generated by Django 5.1 on 2024-11-02 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0050_alter_producto_presupuesto_adicional'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='presupuesto_total',
        ),
    ]
