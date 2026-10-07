from decimal import Decimal
from app.services.parser_service import parse_transaction_message


def test_simple_expense():
    result = parse_transaction_message("350 кофе")
    assert result is not None
    assert result["amount"] == Decimal("350")
    assert result["comment"] == "кофе"
    assert result["operation"] == "-"


def test_income():
    result = parse_transaction_message("+50000 зарплата")
    assert result is not None
    assert result["amount"] == Decimal("50000")
    assert result["comment"] == "зарплата"
    assert result["operation"] == "+"


def test_with_cents():
    result = parse_transaction_message("500.50 обед")
    assert result is not None
    assert result["amount"] == Decimal("500.50")
    assert result["comment"] == "обед"


def test_invalid_format():
    result = parse_transaction_message("просто текст")
    assert result is None