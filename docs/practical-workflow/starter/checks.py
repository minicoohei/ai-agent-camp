"""変更しない固定テスト。初期版は2失敗、修正版は4成功。"""

import unittest

from quote import apply_discount, calculate_quote, calculate_subtotal


class QuoteChecks(unittest.TestCase):
    def test_subtotal_includes_last_item(self):
        self.assertEqual(calculate_subtotal([(20_000, 2), (5_000, 3)]), 55_000)

    def test_discount_at_threshold(self):
        self.assertEqual(apply_discount(100_000), 95_000)

    def test_no_discount_below_threshold(self):
        self.assertEqual(apply_discount(99_999), 99_999)

    def test_quote_above_threshold(self):
        self.assertEqual(
            calculate_quote([(40_000, 2), (30_000, 1), (0, 1)]),
            {"subtotal": 110_000, "discounted": 104_500,
             "tax": 10_450, "total": 114_950},
        )


if __name__ == "__main__":
    unittest.main()
