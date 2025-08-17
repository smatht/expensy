from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from data.models import Categories, Records
from api.serializers.models import (
    CategoriesSerializer,
    RecordsSerializer,
    RecordsListSerializer,
)


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Categories que proporciona
    operaciones CRUD completas
    """

    queryset = Categories.objects.all().order_by("name")
    serializer_class = CategoriesSerializer
    permission_classes = []


class RecordsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Records que proporciona operaciones CRUD completas
    """

    queryset = Records.objects.all().order_by("-date", "-time")
    serializer_class = RecordsSerializer
    permission_classes = []

    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == "list":
            return RecordsListSerializer
        return RecordsSerializer
