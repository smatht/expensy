"""Serializers for converting database records to formatted data structures."""
from typing import List, Union


def records_serializer(
    queryset: List[tuple]
) -> List[List[Union[str, int, float]]]:
    """
    Convert a queryset to a formatted list structure.

    This function takes a queryset of database records and converts each record
    into a standardized list format with proper data type handling.

    Args:
        queryset: List of tuples containing record data in the format:
                 (id, description, date, category, amount, source)

    Returns:
        List of lists, where each inner list represents a formatted record

    Examples:
        >>> records = [(1, "Groceries", datetime(2024, 1, 15),
        ...            "Food", 50.25, "Bank")]
        >>> records_serializer(records)
        [[1, "Groceries", "2024-01-15", "Food", "50.25", "Bank"]]
    """
    formatted_data = []

    for record in queryset:
        formatted_record = [
            record[0],  # id
            record[1] or '',  # description
            record[2].strftime('%Y-%m-%d') if record[2] else '',  # date
            record[3] or '',  # category
            str(record[4]) if record[4] else '',  # amount
            record[5] or ''   # source
        ]
        formatted_data.append(formatted_record)

    return formatted_data
