# Generated by Django 5.1 on 2024-11-07 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0056_usuario_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='Imagen',
            field=models.ImageField(blank=True, null=True, upload_to='usuarios'),
        ),
    ]
