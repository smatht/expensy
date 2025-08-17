from rest_framework import serializers
from data.models import Categories, Records


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categories"""

    class Meta:
        model = Categories
        fields = ["id", "name", "alt_name"]
        read_only_fields = ["id"]


class RecordsSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Records"""

    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Records
        fields = [
            "id",
            "description",
            "date",
            "time",
            "category",
            "category_name",
            "amount",
            "sync",
            "source",
        ]
        read_only_fields = ["id"]


class RecordsListSerializer(serializers.ModelSerializer):
    """Serializer para listar Records con información de categoría"""

    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Records
        fields = [
            "id",
            "description",
            "date",
            "time",
            "category_name",
            "amount",
            "sync",
            "source",
        ]
