from rest_framework import serializers
from .models import DataFile, ColumnInfo

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = '__all__'

class ColumnInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnInfo
        fields = '__all__'