# Generated by Django 5.1 on 2024-11-02 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0047_remove_producto_prioridad'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Prioridad',
            field=models.CharField(choices=[('ALTA', 'Alta'), ('MEDIA', 'Media'), ('BAJA', 'Baja')], default='MEDIA', max_length=5),
        ),
        migrations.AddField(
            model_name='producto',
            name='porcentaje_utilizado',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]
