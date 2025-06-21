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


from celery import shared_task
from .models import Estrategia
from integraciones.trading_logic import TradingEngine


@shared_task
def procesar_estrategias_activas():
    estrategias = Estrategia.objects.filter(activo=True)
    engine = TradingEngine()
    
    for estrategia in estrategias:
        procesar_estrategia.delay(str(estrategia.id))

@shared_task
def procesar_estrategia(estrategia_id: str):
    try:
        estrategia = Estrategia.objects.get(id=estrategia_id)
        engine = TradingEngine()
        senal = engine.procesar_estrategia(estrategia)
        
        if senal:
            engine.ejecutar_senal(senal)
    except Estrategia.DoesNotExist:
        print(f"Estrategia {estrategia_id} no encontrada")
    except Exception as e:
        print(f"Error procesando estrategia {estrategia_id}: {e}")