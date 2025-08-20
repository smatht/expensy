"""Google Cloud Function for loading and synchronizing records to Google Sheets."""

import os
import logging
import requests
import functions_framework

from typing import List, Dict, Any
from datetime import datetime

from .google_sheet_actions import GoogleSheet

# Google Sheets configuration
DOCUMENT_NAME = "Expensy"
SHEET_NAME = "records"

# API configuration - these should be set as environment variables in GCP
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api")


def records_serializer(records_data: List[Dict[str, Any]]) -> List[List[str]]:
    """
    Convert API records data to a formatted list structure for Google Sheets.

    Args:
        records_data: List of dictionaries containing record data from API

    Returns:
        List of lists, where each inner list represents a formatted record

    Examples:
        >>> records = [{"id": "123", "description": "Groceries",
        ...            "date": "2024-01-15", "category_name": "Food",
        ...            "amount": "50.25", "source": "Bank"}]
        >>> records_serializer(records)
        [["123", "Groceries", "2024-01-15", "Food", "50.25", "Bank"]]
    """
    formatted_data = []

    for record in records_data:
        # Format date if it exists
        date_str = ""
        if record.get("date"):
            try:
                # Parse date string and format it
                date_obj = datetime.fromisoformat(
                    record["date"].replace("Z", "+00:00")
                )
                date_str = date_obj.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                date_str = str(record["date"]) if record["date"] else ""

        formatted_record = [
            record.get("id", ""),
            record.get("description", "") or "",
            date_str,
            record.get("category_name", "") or "",
            str(record.get("amount", "")) if record.get("amount") else "",
            record.get("source", "") or ""
        ]
        formatted_data.append(formatted_record)

    return formatted_data


def get_unsynced_records() -> List[Dict[str, Any]]:
    """
    Fetch unsynchronized records from the API.

    Returns:
        List of record dictionaries from the API

    Raises:
        requests.RequestException: If the API request fails
    """
    print("getting unsynced records")
    url = f"{API_BASE_URL}/records/"
    print(f"url: {url}")
    params = {"sync": "false"}

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["results"]


def bulk_sync_records(record_ids: List[str]) -> bool:
    """
    Mark multiple records as synchronized via API.

    Args:
        record_ids: List of record IDs to mark as synced

    Returns:
        True if successful, False otherwise

    Raises:
        requests.RequestException: If the API request fails
    """
    if not record_ids:
        return True

    url = f"{API_BASE_URL}/records/bulk-sync/"
    payload = {"record_ids": record_ids}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return True


@functions_framework.http
def load_records_to_sheet_cloud_function(request):
    """
    Google Cloud Function entry point for loading records to Google Sheets.

    This function:
    1. Retrieves all unsynchronized records from the API
    2. Serializes them using the records_serializer
    3. Writes the data to Google Sheets
    4. Marks all processed records as synchronized via API

    Args:
        request: Flask request object (Google Cloud Functions)

    Returns:
        JSON response with status and details
    """
    try:
        # Initialize Google Sheets connection
        # In GCP, the service account credentials are automatically available
        logging.info("Starting process...")
        print("SStarting process...")
        google = GoogleSheet(None, DOCUMENT_NAME, SHEET_NAME)

        # Get unsynchronized records from API
        records_data = get_unsynced_records()

        if not records_data:
            return {
                "status": "success",
                "message": "No unsynchronized records found",
                "records_processed": 0
            }

        # Serialize records for Google Sheets
        serialized_data = records_serializer(records_data)

        # Get the range for writing data
        data_range = google.get_last_row_range(amount_rows=len(serialized_data))

        # Write data to Google Sheets
        google.write_data(data_range, serialized_data)

        # Extract record IDs for bulk sync
        record_ids = [record["id"] for record in records_data]

        # Mark all processed records as synchronized via API
        bulk_sync_records(record_ids)

        return {
            "status": "success",
            "message": (
                f"Successfully processed {len(records_data)} records"
            ),
            "records_processed": len(records_data),
            "data_range": data_range
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "message": f"API request failed: {str(e)}",
            "error_type": "api_error"
        }, 500

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "error_type": "general_error"
        }, 500
