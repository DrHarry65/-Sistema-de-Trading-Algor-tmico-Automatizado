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

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_backend.settings')

app = Celery('trading_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Tarea periódica para procesar estrategias
app.conf.beat_schedule = {
    'procesar-estrategias-cada-5-min': {
        'task': 'estrategias.tasks.procesar_estrategias_activas',
        'schedule': 300.0,  # Cada 5 minutos
    },
}