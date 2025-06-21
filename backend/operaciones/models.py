# trading_logic.py
# Copyright (C) 2025 Alejandro Rodriguez
# This file is part of ProyectoNombre.
#
# ProyectoNombre is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ProyectoNombre is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import uuid
from django.db import models
from estrategias.models import Estrategia

class Operacion(models.Model):
    TIPO_CHOICES = [
        ('BUY', 'Compra'),
        ('SELL', 'Venta'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('OPEN', 'Abierta'),
        ('CLOSED', 'Cerrada'),
        ('CANCELED', 'Cancelada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE, related_name='operaciones')
    simbolo = models.CharField(max_length=20)  # Ej: 'BTCUSDT'
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    precio_entrada = models.DecimalField(max_digits=20, decimal_places=8)
    precio_salida = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=20, decimal_places=8)
    ganancia_perdida = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='PENDING')
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} {self.simbolo} @ {self.precio_entrada}"