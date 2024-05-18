# internal_db_ops/views.py
from rest_framework import viewsets
from .models import InternalItem
from .serializers import InternalItemSerializer

class InternalItemViewSet(viewsets.ModelViewSet):
    queryset = InternalItem.objects.all()
    serializer_class = InternalItemSerializer
