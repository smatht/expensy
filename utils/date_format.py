from datetime import date
from typing import Dict

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

# Diccionario para las abreviaciones de meses (reutilizando MONTHS)
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
    Parse a string in the form "<Spanish_month> <year>" and return
    a date object set to the first day of that month and year.

    Examples:
        >>> parse_month_year("Junio 2025")
        datetime.date(2025, 6, 1)
    """
    parts = input_str.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Invalid format, expected '<month> <year>', got: {input_str!r}")

    month_str, year_str = parts
    month_num = MONTHS.get(month_str.lower())
    if month_num is None:
        raise ValueError(f"Unknown month name: {month_str!r}")

    try:
        year = int(year_str)
    except ValueError:
        raise ValueError(f"Invalid year value: {year_str!r}")

    return date(year, month_num, 1)


def parse_day_month(input_str: str, year: int = None) -> date:
    """
    Parse a string in the form "<day>/<Spanish_month_abbreviation>" and return
    a date object for that day and month. If year is not provided, uses current year.

    Examples:
        >>> parse_day_month("1/jun", 2025)
        datetime.date(2025, 6, 1)
        >>> parse_day_month("22/ene", 2024)
        datetime.date(2024, 1, 22)
    """
    if year is None:
        year = date.today().year

    if "hs" in input_str:
        return date.today()

    parts = input_str.strip().split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid format, expected '<day>/<month>', got: {input_str!r}")

    day_str, month_str = parts

    # Validar día
    try:
        day = int(day_str)
    except ValueError:
        raise ValueError(f"Invalid day value: {day_str!r}")

    # Buscar mes abreviado
    month_num = MONTH_ABBREVIATIONS.get(month_str.lower())
    if month_num is None:
        raise ValueError(f"Unknown month abbreviation: {month_str!r}")
    try:
        return date(year, month_num, day)
    except ValueError as e:
        raise ValueError(f"Invalid date:{e}")
