"""
Đọc tham số GET an toàn (tránh lỗi khi người dùng sửa URL tay).
"""
from decimal import Decimal, InvalidOperation


def parse_positive_int(value):
    """Trả về số nguyên dương hoặc None nếu không hợp lệ."""
    if value is None or value == "":
        return None
    try:
        n = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def parse_decimal(value):
    """Trả về Decimal nếu là số hợp lệ, không thì None."""
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value).strip().replace(",", "."))
    except (InvalidOperation, ValueError, TypeError):
        return None
