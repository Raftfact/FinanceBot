import re
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation


def parse_transaction_message(text: str) -> Tuple[Optional[Decimal], str]:
    """
    Парсит сообщение вида "350 кофе" или "5000 зарплата"
    Возвращает (amount, comment)
    """
    text = text.strip()
    
    match = re.match(r'^(\d+(?:[.,]\d{1,2})?)\s+(.+)$', text)
    
    if not match:
        return None, text
    
    amount_str = match.group(1).replace(',', '.')
    comment = match.group(2).strip()
    
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return None, text
        return amount, comment
    except InvalidOperation:
        return None, text


def determine_category_by_comment(comment: str) -> Optional[str]:
    comment_lower = comment.lower()
    
    category_keywords = {
        "Еда": ["кофе", "чай", "хлеб", "молоко", "ресторан", "кафе", "обед", "ужин"],
        "Транспорт": ["такси", "метро", "бензин", "автобус", "электричка"],
        "Развлечения": ["кино", "театр", "концерт", "игр", "подписк"],
        "Зарплата": ["зарплата", "зарплат", "аванс"],
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in comment_lower for keyword in keywords):
            return category
    
    return "Прочее"