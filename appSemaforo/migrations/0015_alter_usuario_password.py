# Generated by Django 5.1 on 2024-09-09 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0014_alter_usuario_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
