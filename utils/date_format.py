"""Date formatting utilities for parsing various date formats."""

from datetime import date
from typing import Dict, Optional
from django.utils.dateparse import parse_date


# Spanish month names mapping
MONTHS: Dict[str, int] = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12,
}

# Spanish month abbreviations mapping
MONTH_ABBREVIATIONS: Dict[str, int] = {
    'ene': MONTHS['enero'],
    'feb': MONTHS['febrero'],
    'mar': MONTHS['marzo'],
    'abr': MONTHS['abril'],
    'may': MONTHS['mayo'],
    'jun': MONTHS['junio'],
    'jul': MONTHS['julio'],
    'ago': MONTHS['agosto'],
    'sep': MONTHS['septiembre'],
    'oct': MONTHS['octubre'],
    'nov': MONTHS['noviembre'],
    'dic': MONTHS['diciembre'],
}


def parse_month_year(input_str: str) -> date:
    """
    Parse a string in the form "<Spanish_month> <year>" and return a date.

    Args:
        input_str: String in format "Month Year" (e.g., "Junio 2025")

    Returns:
        Date object set to the first day of that month and year

    Raises:
        ValueError: If the format is invalid or month/year values are invalid

    Examples:
        >>> parse_month_year("Junio 2025")
        datetime.date(2025, 6, 1)
        >>> parse_month_year("Diciembre 2024")
        datetime.date(2024, 12, 1)
    """
    parts = input_str.strip().split()
    if len(parts) != 2:
        raise ValueError(
            f"Invalid format, expected '<month> <year>', got: {input_str!r}"
        )

    month_str, year_str = parts
    month_num = MONTHS.get(month_str.lower())
    if month_num is None:
        raise ValueError(f"Unknown month name: {month_str!r}")

    try:
        year = int(year_str)
    except ValueError:
        raise ValueError(f"Invalid year value: {year_str!r}")

    return date(year, month_num, 1)


def parse_day_month(
    input_str: str, year: Optional[int] = None, month: Optional[int] = None
) -> date:
    """
    Parse a string in the form "<day>/<Spanish_month_abbreviation>" and return a date.

    Args:
        input_str: String in format "day/month_abbr" (e.g., "1/jun")
        year: Year to use (defaults to current year if not provided)
        month: Month to use (overrides month from input_str if provided)

    Returns:
        Date object for the specified day and month

    Raises:
        ValueError: If the format is invalid or date values are invalid

    Examples:
        >>> parse_day_month("1/jun", 2025)
        datetime.date(2025, 6, 1)
        >>> parse_day_month("22/ene", 2024)
        datetime.date(2024, 1, 22)
        >>> parse_day_month("15/mar")
        datetime.date(2024, 3, 15)  # Uses current year
    """
    if year is None:
        year = date.today().year

    # Handle special case for "hs" (hours)
    if "hs" in input_str:
        return date.today()

    parts = input_str.strip().split('/')
    if len(parts) != 2:
        raise ValueError(
            f"Invalid format, expected '<day>/<month>', got: {input_str!r}"
        )

    day_str, month_str = parts

    # Validate day
    try:
        day = int(day_str)
    except ValueError:
        raise ValueError(f"Invalid day value: {day_str!r}")

    # Get month number
    if month is not None:
        month_num = month
    else:
        month_num = MONTH_ABBREVIATIONS.get(month_str.lower())
        if month_num is None:
            raise ValueError(f"Unknown month abbreviation: {month_str!r}")

    try:
        return date(year, month_num, day)
    except ValueError as e:
        print(f"ERROR: Invalid date: {e}")
        return date(year, month_num, 1)


def parse_day_month_year(date_str: str) -> Optional[date]:
    """
    Convert date format dd/mm/yyyy to yyyy-mm-dd and parse it.

    Args:
        date_str: Date string in format "dd/mm/yyyy"

    Returns:
        Parsed date object or None if parsing fails

    Examples:
        >>> parse_day_month_year("25/12/2024")
        datetime.date(2024, 12, 25)
        >>> parse_day_month_year("01/01/2025")
        datetime.date(2025, 1, 1)
    """
    parts = date_str.split('/')
    if len(parts) != 3:
        raise ValueError(f"Invalid date format: {date_str}")

    date_iso = f"{parts[2]}-{parts[1]}-{parts[0]}"
    return parse_date(date_iso)
