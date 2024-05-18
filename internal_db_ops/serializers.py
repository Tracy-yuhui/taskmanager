# internal_db_ops/serializers.py
from rest_framework import serializers
from .models import InternalItem

class InternalItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalItem
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
