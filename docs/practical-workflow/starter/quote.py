"""架空の見積計算。演習用の不具合を2か所含む初期版。"""

from decimal import Decimal, ROUND_HALF_UP

DISCOUNT_THRESHOLD = 100_000
DISCOUNT_RATE = Decimal("0.05")
TAX_RATE = Decimal("0.10")


def calculate_subtotal(items: list[tuple[int, int]]) -> int:
    """(単価, 数量) の一覧から小計を返す。"""
    return sum(unit_price * quantity for unit_price, quantity in items[:-1])


def apply_discount(subtotal: int) -> int:
    """対象額へ5%値引きを適用し、1円単位で四捨五入する。"""
    if subtotal > DISCOUNT_THRESHOLD:
        return int(
            (Decimal(subtotal) * (Decimal("1") - DISCOUNT_RATE)).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )
    return subtotal


def calculate_quote(items: list[tuple[int, int]]) -> dict[str, int]:
    subtotal = calculate_subtotal(items)
    discounted = apply_discount(subtotal)
    tax = int(
        (Decimal(discounted) * TAX_RATE).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
    )
    return {
        "subtotal": subtotal,
        "discounted": discounted,
        "tax": tax,
        "total": discounted + tax,
    }
