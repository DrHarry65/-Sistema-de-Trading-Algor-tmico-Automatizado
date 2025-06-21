from rest_framework import serializers
from senales.models import Senal

class SenalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Senal
        fields = [
            'id',
            'estrategia',
            'simbolo',
            'tipo',
            'precio',
            'indicadores_valores',
            'procesada',
            'fecha_generacion'
        ]
        read_only_fields = ['id', 'fecha_generacion']