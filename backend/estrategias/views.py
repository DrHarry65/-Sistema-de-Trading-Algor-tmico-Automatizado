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

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Estrategia
from .serializers import EstrategiaSerializer, EstrategiaCreateSerializer

class EstrategiaViewSet(viewsets.ModelViewSet):
    queryset = Estrategia.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EstrategiaCreateSerializer
        return EstrategiaSerializer
    
    def perform_create(self, serializer):
        serializer.save(activo=False)
    
    def activate(self, request, pk=None):
        estrategia = self.get_object()
        estrategia.activo = True
        estrategia.save()
        return Response({'status': 'estrategia activada'})
    
    def deactivate(self, request, pk=None):
        estrategia = self.get_object()
        estrategia.activo = False
        estrategia.save()
        return Response({'status': 'estrategia desactivada'})
