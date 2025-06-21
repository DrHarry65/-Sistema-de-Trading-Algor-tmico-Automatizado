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

class Senal(models.Model):
    TIPO_CHOICES = [
        ('BUY', 'Compra'),
        ('SELL', 'Venta'),
        ('ALERT', 'Alerta'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE, related_name='senales')
    simbolo = models.CharField(max_length=20)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    precio = models.DecimalField(max_digits=20, decimal_places=8)
    indicadores_valores = models.JSONField()  # Valores de los indicadores al momento de la señal
    procesada = models.BooleanField(default=False)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} {self.simbolo} @ {self.precio}"
