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
            name='Operacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('simbolo', models.CharField(max_length=20)),
                ('tipo', models.CharField(choices=[('BUY', 'Compra'), ('SELL', 'Venta')], max_length=4)),
                ('precio_entrada', models.DecimalField(decimal_places=8, max_digits=20)),
                ('precio_salida', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('cantidad', models.DecimalField(decimal_places=8, max_digits=20)),
                ('ganancia_perdida', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('estado', models.CharField(choices=[('PENDING', 'Pendiente'), ('OPEN', 'Abierta'), ('CLOSED', 'Cerrada'), ('CANCELED', 'Cancelada')], default='PENDING', max_length=8)),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('stop_loss', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('take_profit', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('estrategia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operaciones', to='estrategias.estrategia')),
            ],
        ),
    ]
