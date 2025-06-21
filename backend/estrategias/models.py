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
from django.utils import timezone

class Estrategia(models.Model):
    TIMEFRAME_CHOICES = [
        ('1h', '1 Hora'),
        ('4h', '4 Horas'),
        ('1d', '1 Día'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    indicadores = models.JSONField()  # Almacena configuración de indicadores
    timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES)
    activo = models.BooleanField(default=False)
    parametros = models.JSONField()  # Parámetros adicionales
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_timeframe_display()})"
