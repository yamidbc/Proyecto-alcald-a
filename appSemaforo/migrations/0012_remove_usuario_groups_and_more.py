# Generated by Django 5.1 on 2024-09-09 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0011_rename_superusuario_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
    ]
