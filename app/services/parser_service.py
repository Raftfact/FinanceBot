from typing import Optional, Dict
from decimal import Decimal, InvalidOperation


def parse_transaction_message(text: str) -> Optional[Dict]:
    text = text.strip()

    transaction = {
        "amount": None,
        "operation": None,
        "comment": None
    }

    digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if text[0] == '+':
        transaction["operation"] = "+"
        text = text[1:].strip()
    elif text[0] == '-':
        transaction["operation"] = "-"
        text = text[1:].strip()
    elif text[0] in digit:
        transaction["operation"] = "-"
    else:
        return None

    amount_str = ""
    for i in text:
        if i not in digit and i != "." and i != ",":
            break
        amount_str += i

    text = text[len(amount_str):].strip()

    if not amount_str:
        return None

    try:
        amount = Decimal(amount_str.replace(',', '.'))
        if amount <= 0:
            return None
        transaction["amount"] = amount
    except InvalidOperation:
        return None

    transaction["comment"] = text if text else None

    return transaction