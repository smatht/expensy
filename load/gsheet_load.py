import os

from django.core.wsgi import get_wsgi_application

from serializers.records import records_serializer
from services.google_sheet_actions import GoogleSheet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()
from data.models import Records

FILE_NAME_SA = "E:\expensy-465801-22bce19d4412.json"
DOCUMENT_NAME = "Expensy"
SHEET_NAME = "records"


def sync_record(record_id):
    Records.objects.filter(pk=record_id).update(sync=True)


if __name__ == '__main__':
    google = GoogleSheet(FILE_NAME_SA, DOCUMENT_NAME, SHEET_NAME)

    queryset = Records.objects.filter(sync=False).values_list("id", "description", "date", "category__name", "amount", "source")

    value = records_serializer(queryset)
    range = google.get_last_row_range(amount_rows=len(value))
    google.write_data(range, value)

    for record in queryset:
        sync_record(record[0])
