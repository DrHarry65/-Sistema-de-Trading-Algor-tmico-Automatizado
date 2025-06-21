"""
URL configuration for trading_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
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

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from estrategias.views import EstrategiaViewSet
from senales.views import SenalViewSet

router = DefaultRouter()
router.register(r'estrategias', EstrategiaViewSet, basename='estrategia')

# Crea un router y registra el ViewSet
router = DefaultRouter()
router.register(r'senales', SenalViewSet, basename='senal')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/estrategias/<uuid:pk>/activate/', EstrategiaViewSet.as_view({'post': 'activate'})),
    path('api/estrategias/<uuid:pk>/deactivate/', EstrategiaViewSet.as_view({'post': 'deactivate'})),
    path('api/', include(router.urls)),
]