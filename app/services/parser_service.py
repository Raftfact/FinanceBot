import re
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation


def parse_transaction_message(text: str):
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

    for i in text:
        if i not in digit and i != "." and i != ",":
            break
        transaction["amount"] = (transaction["amount"] or "") + i

    text = text[len(transaction["amount"]):].strip()

    if transaction["amount"] is None:
        return None

    transaction["comment"] = text if text else None

    return transaction