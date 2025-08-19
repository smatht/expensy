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


class RecordsBulkSyncSerializer(serializers.Serializer):
    """Serializer para operación bulk de sincronización de records"""

    record_ids = serializers.ListField(
        child=serializers.CharField(max_length=40),
        min_length=1,
        max_length=1000,
        help_text=("Lista de IDs de records a marcar como sincronizados"),
    )

    def validate_record_ids(self, value):
        """Validar que los IDs existen en la base de datos"""
        from data.models import Records

        # Verificar que todos los IDs existen
        existing_ids = set(
            Records.objects.filter(id__in=value).values_list("id", flat=True)
        )
        invalid_ids = set(value) - existing_ids

        if invalid_ids:
            raise serializers.ValidationError(
                f"Los siguientes IDs no existen: {list(invalid_ids)}"
            )

        return value


class CategoryReportSerializer(serializers.Serializer):
    """Serializer para el reporte de categorías por mes"""

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    categories = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
