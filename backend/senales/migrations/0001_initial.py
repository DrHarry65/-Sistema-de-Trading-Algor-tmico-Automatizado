# Generated by Django 5.2.3 on 2025-06-21 15:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estrategias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Senal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('simbolo', models.CharField(max_length=20)),
                ('tipo', models.CharField(choices=[('BUY', 'Compra'), ('SELL', 'Venta'), ('ALERT', 'Alerta')], max_length=5)),
                ('precio', models.DecimalField(decimal_places=8, max_digits=20)),
                ('indicadores_valores', models.JSONField()),
                ('procesada', models.BooleanField(default=False)),
                ('fecha_generacion', models.DateTimeField(auto_now_add=True)),
                ('estrategia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senales', to='estrategias.estrategia')),
            ],
        ),
    ]
