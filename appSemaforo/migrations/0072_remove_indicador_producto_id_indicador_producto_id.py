# Generated by Django 5.1 on 2024-11-19 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0071_indicador_producto_codigo_indicador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicador_producto',
            name='ID',
        ),
        migrations.AddField(
            model_name='indicador_producto',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
