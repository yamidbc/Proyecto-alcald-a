# Generated by Django 5.1 on 2024-11-09 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0060_producto_status_meta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicoproducto',
            name='Descripción',
        ),
        migrations.RemoveField(
            model_name='historicoproducto',
            name='Soporte',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='Status_Meta',
        ),
    ]
