# Generated by Django 5.1 on 2024-09-19 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0025_remove_producto_progreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Soporte',
            field=models.FileField(default=1, upload_to='archivos/'),
            preserve_default=False,
        ),
    ]
