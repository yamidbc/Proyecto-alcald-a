# Generated by Django 5.1 on 2024-09-17 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSemaforo', '0023_rename_id_producto_id_producto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Valor_actual',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
