import re


def macro_inference(evaluate_text: str) -> int:
    EXPENSE_DPEC_REGEX = r"(?=.*PAGOS360)(?=.*DPEC)"
    EXPENSE_AGUAS_REGEX = r"(?=.*PAGOS360)(?=.*AGUASCORRIENT)"
    EXPENSE_CREDIT_VISA_REGEX = r".*DB TARJETA DE CREDITO VISA.*"
    EXPENSE_LOANS_REGEX = r".*DEBITO PRESTAMOS.*"
    DEFAULT_RESULT = 0

    map_match = {
        3: [EXPENSE_DPEC_REGEX, EXPENSE_AGUAS_REGEX, EXPENSE_CREDIT_VISA_REGEX],
        14: [EXPENSE_LOANS_REGEX]
    }

    for item in map_match.keys():
        for expresion in map_match[item]:
            regex = re.compile(expresion)
            match = regex.match(evaluate_text)
            if match:
                return item
    return DEFAULT_RESULT
