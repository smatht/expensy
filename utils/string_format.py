import re


def parse_amount_to_float(amount_str):
    """
    Converts a Spanish natural language amount string to float.

    Args:
        amount_str (str): Amount string (e.g., '-8868 pesos con 06 centavos')

    Returns:
        float: The numeric value of the amount

    Examples:
        >>> parse_amount_to_float('-8868 pesos con 06 centavos')
        -8868.06
        >>> parse_amount_to_float('-3559 pesos con 69 centavos')
        -3559.69
        >>> parse_amount_to_float('-828200 pesos')
        -828200.0
    """
    if not amount_str or not isinstance(amount_str, str):
        return 0.0

    # Clean the string
    amount_str = amount_str.strip()

    # Pattern to capture: optional sign, pesos, and optional centavos
    pattern = r'^([+-]?)(\d+)\s*pesos(?:\s+con\s+(\d+)\s+centavos)?'

    match = re.match(pattern, amount_str, re.IGNORECASE)

    if not match:
        raise ValueError(f"Invalid amount format: {amount_str}")

    sign, pesos, centavos = match.groups()

    # Convert to numbers
    peso_value = int(pesos)
    centavo_value = int(centavos) if centavos else 0

    # Build the final value
    result = peso_value + (centavo_value / 100)

    # Apply negative sign if present
    if sign == '-':
        result = -result

    return result