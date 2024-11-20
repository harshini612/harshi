from rest_framework import serializers
from .models import swag
class swagserializer(serializers.ModelSerializer):
    class Meta:
        model= swag
        fields="__all__"
