"""Category inference utilities for transaction classification."""

import re
from typing import Dict, List


def macro_inference(evaluate_text: str) -> int:
    """
    Infer transaction category based on text patterns.

    This function uses regex patterns to classify transactions into categories
    based on the transaction description text.

    Args:
        evaluate_text: The transaction description text to analyze

    Returns:
        Category ID as integer. Returns 0 if no match is found.

    Examples:
        >>> macro_inference("PAGOS360 DPEC")
        3
        >>> macro_inference("MERCADOLIBRE SRL 30703088534")
        21
        >>> macro_inference("Unknown transaction")
        0
    """
    # Regex patterns for different transaction types
    EXPENSE_DPEC_REGEX = r"(?=.*PAGOS360)(?=.*DPEC)"
    EXPENSE_AGUAS_REGEX = r"(?=.*PAGOS360)(?=.*AGUASCORRIENT)"
    EXPENSE_CREDIT_VISA_REGEX = r".*DB TARJETA DE CREDITO VISA.*"
    EXPENSE_LOANS_REGEX = r".*DEBITO PRESTAMOS.*"
    INCOME_MELI_REGEX = r".*MERCADOLIBRE SRL 30703088534.*"
    DEFAULT_RESULT = 0

    # Map category IDs to their corresponding regex patterns
    category_patterns: Dict[int, List[str]] = {
        3: [
            EXPENSE_DPEC_REGEX,
            EXPENSE_AGUAS_REGEX,
            EXPENSE_CREDIT_VISA_REGEX
        ],
        14: [EXPENSE_LOANS_REGEX],
        21: [INCOME_MELI_REGEX]
    }

    # Check each category's patterns
    for category_id, patterns in category_patterns.items():
        for pattern in patterns:
            regex = re.compile(pattern)
            match = regex.match(evaluate_text)
            if match:
                return category_id

    return DEFAULT_RESULT
