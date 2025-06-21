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

from rest_framework import serializers
from .models import Estrategia

class EstrategiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estrategia
        fields = '__all__'
        read_only_fields = ('id', 'fecha_creacion', 'fecha_modificacion')

class EstrategiaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estrategia
        fields = ['nombre', 'descripcion', 'indicadores', 'timeframe', 'parametros']