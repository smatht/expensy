from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from data.models import Categories, Records
from api.serializers.models import (
    CategoriesSerializer,
    RecordsSerializer,
    RecordsListSerializer,
    CategoryReportSerializer,
)
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
import calendar


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Categories model that provides
    complete CRUD operations
    """

    queryset = Categories.objects.all().order_by("name")
    serializer_class = CategoriesSerializer
    permission_classes = []

    @action(detail=False, methods=["get"], url_path="monthly-report")
    def monthly_report(self, request):
        """
        Returns a monthly report of records summarized by categories.
        Parameters:
        - month: month number (1-12), defaults to current month
        - year: year number, defaults to current year
        """
        # Get month and year parameters, default to current date
        current_date = timezone.now()
        month = request.query_params.get("month", current_date.month)
        year = request.query_params.get("year", current_date.year)

        try:
            month = int(month)
            year = int(year)


            # Validate month range
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")

            # Validate year (reasonable range)
            if year < 1900 or year > 2100:
                raise ValueError("Year must be between 1900 and 2100")

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Get the first and last day of the month
        first_day = datetime(year, month, 1).date()
        last_day = datetime(year, month, 31).date()

        # Adjust last day for months with fewer days
        last_day = min(
            last_day, datetime(year, month, calendar.monthrange(year, month)[1]).date()
        )

        # Query records for the specified month and aggregate by category
        records = (
            Records.objects.filter(date__gte=first_day, date__lte=last_day)
            .values("category__name")
            .annotate(total_amount=Sum("amount"))
            .order_by("category__name")
        )

        # Build the categories dictionary
        categories_dict = {}
        total_sum = 0

        for record in records:
            category_name = record["category__name"] or "Sin categoría"
            amount = record["total_amount"]
            categories_dict[category_name] = amount
            total_sum += amount

        # Prepare response data
        report_data = {
            "month": month,
            "year": year,
            "categories": categories_dict,
            "total": total_sum,
        }

        # Validate with serializer
        serializer = CategoryReportSerializer(data=report_data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecordsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Records model that provides complete CRUD operations
    """

    queryset = Records.objects.all().order_by("-date", "-time")
    serializer_class = RecordsSerializer
    permission_classes = []

    def get_serializer_class(self):
        """Returns the appropriate serializer based on the action"""
        if self.action == "list":
            return RecordsListSerializer
        return RecordsSerializer

    @action(detail=False, methods=["get"], url_path="recents")
    def recents(self, request):
        """
        Returns the most recent records loaded, ordered by date.
        Receives a 'size' parameter to limit the number of records
        (maximum 100).
        """
        # Get the size parameter from the query
        size_param = request.query_params.get("size", "10")

        try:
            size = int(size_param)
        except ValueError:
            raise ValidationError("The 'size' parameter must be a valid integer")

        # Validate that size doesn't exceed 100 records
        if size > 100:
            raise ValidationError("The 'size' parameter cannot exceed 100 records")

        # Validate that size is positive
        if size <= 0:
            raise ValidationError("The 'size' parameter must be a positive number")

        # Get the most recent records ordered by date
        # (most recent first)
        recent_records = Records.objects.all().order_by("-date", "-time")[:size]

        # Serialize the results
        serializer = RecordsListSerializer(recent_records, many=True)

        return Response(
            {"count": len(recent_records), "size": size, "results": serializer.data}
        )
