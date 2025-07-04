# Generated by Django 5.2.3 on 2025-06-21 15:12

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estrategia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('indicadores', models.JSONField()),
                ('timeframe', models.CharField(choices=[('1h', '1 Hora'), ('4h', '4 Horas'), ('1d', '1 Día')], max_length=10)),
                ('activo', models.BooleanField(default=False)),
                ('parametros', models.JSONField()),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
