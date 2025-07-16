"""Google Sheets data loading and synchronization module."""

import os

from django.core.wsgi import get_wsgi_application

from serializers.records import records_serializer
from services.google_sheet_actions import GoogleSheet

# Django configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()

from data.models import Records

# Google Sheets configuration
FILE_NAME_SA = "E:\\expensy-465801-22bce19d4412.json"
DOCUMENT_NAME = "Expensy"
SHEET_NAME = "records"


def sync_record(record_id: int) -> None:
    """
    Mark a record as synchronized in the database.

    Args:
        record_id: The ID of the record to mark as synced
    """
    Records.objects.filter(pk=record_id).update(sync=True)


def load_records_to_sheet() -> None:
    """
    Load unsynchronized records from database to Google Sheets.

    This function:
    1. Retrieves all unsynchronized records from the database
    2. Serializes them using the records_serializer
    3. Writes the data to Google Sheets
    4. Marks all processed records as synchronized
    """
    # Initialize Google Sheets connection
    google = GoogleSheet(FILE_NAME_SA, DOCUMENT_NAME, SHEET_NAME)

    # Get unsynchronized records from database
    queryset = Records.objects.filter(sync=False).values_list(
        "id", "description", "date", "category__name", "amount", "source"
    )

    # Serialize records for Google Sheets
    serialized_data = records_serializer(queryset)

    # Get the range for writing data
    data_range = google.get_last_row_range(amount_rows=len(serialized_data))

    # Write data to Google Sheets
    google.write_data(data_range, serialized_data)

    # Mark all processed records as synchronized
    for record in queryset:
        sync_record(record[0])


if __name__ == '_main_':
    load_records_to_sheet()
