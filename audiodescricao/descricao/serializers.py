from rest_framework import serializers
from .models import Imagem

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = ['id', 'imagem', 'descricao', 'data_captura']
