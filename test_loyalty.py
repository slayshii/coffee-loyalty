import unittest
from loyalty import apply_loyalty_discount, apply_3plus1


class TestApplyLoyaltyDiscount(unittest.TestCase):
    def setUp(self):
        self.four_coffees = [
            {"name": "Латте", "price": 250, "category": "coffee"},
            {"name": "Капучино", "price": 220, "category": "coffee"},
            {"name": "Эспрессо", "price": 150, "category": "coffee"},
            {"name": "Американо", "price": 120, "category": "coffee"},
        ]
        self.alcohol_only = [
            {"name": "Глинтвейн", "price": 300, "category": "alcohol"},
            {"name": "Ликёр", "price": 200, "category": "alcohol"},
        ]

    # apply_loyalty_discount 

    def test_bronze_regular_order(self):
        #Обычный заказ с Bronze: акция + скидка 5%.
        result = apply_loyalty_discount(self.four_coffees, "Bronze")
        # 740 - 120 (бесплатный) = 620, скидка 5% = 31
        self.assertEqual(result["total"], 589.0)
        self.assertEqual(result["discount"], 31.0)
        self.assertEqual(len(result["bonuses"]), 2)

    def test_gold_with_alcohol(self):
        #Заказ с Gold и алкоголем: алкоголь не в акции, но в базе скидки.
        order = self.four_coffees + [
            {"name": "Глинтвейн", "price": 300, "category": "alcohol"}
        ]
        result = apply_loyalty_discount(order, "Gold")
        # База: 1040 - 120 = 920, скидка 15% = 138
        self.assertEqual(result["total"], 782.0)
        self.assertEqual(result["discount"], 138.0)

    def test_none_card(self):
        #Карта 'None': скидка 0, но акция 3+1 работает.
        result = apply_loyalty_discount(self.four_coffees, "None")
        self.assertEqual(result["total"], 600.0)
        self.assertEqual(result["discount"], 0.0)
        self.assertEqual(len(result["bonuses"]), 1)
        self.assertIn("3+1", result["bonuses"][0])

    def test_empty_order(self):
        #Граничный случай: пустой список — нули и никаких бонусов
        result = apply_loyalty_discount([], "Gold")
        self.assertEqual(result["total"], 0.0)
        self.assertEqual(result["discount"], 0.0)
        self.assertEqual(result["bonuses"], [])

    def test_all_alcohol(self):
        #Граничный случай: только алкоголь — без акции, скидка от полной суммы
        result = apply_loyalty_discount(self.alcohol_only, "Silver")
        self.assertEqual(result["total"], 450.0)
        self.assertEqual(result["discount"], 50.0)
        self.assertEqual(len(result["bonuses"]), 1)

    def test_unknown_level_falls_back_to_none(self):
        #Некорректный уровень карты: трактуется как отсутствие карты
        result = apply_loyalty_discount(self.four_coffees, "Platinum")
        self.assertEqual(result["discount"], 0.0)
        self.assertEqual(result["total"], 600.0)

    def test_total_never_negative(self):
        #Итоговая сумма никогда не уходит в минус
        result = apply_loyalty_discount(
            [{"name": "Кофе", "price": 10, "category": "coffee"}], "Gold"
        )
        self.assertGreaterEqual(result["total"], 0.0)


class TestApply3Plus1(unittest.TestCase):
    def setUp(self):
        self.four_drinks = [
            {"name": "A", "price": 100, "category": "coffee"},
            {"name": "B", "price": 80, "category": "coffee"},
            {"name": "C", "price": 70, "category": "coffee"},
            {"name": "D", "price": 50, "category": "coffee"},
        ]
        self.three_drinks = self.four_drinks[:3]

    def test_four_drinks_cheapest_free(self):
        free_sum, free_names = apply_3plus1(self.four_drinks)
        self.assertEqual(free_sum, 50.0)
        self.assertEqual(free_names, ["D"])

    def test_three_drinks_no_promo(self):
        free_sum, free_names = apply_3plus1(self.three_drinks)
        self.assertEqual(free_sum, 0.0)
        self.assertEqual(free_names, [])

    def test_alcohol_not_counted(self):
        items = self.four_drinks + [
            {"name": "Глинтвейн", "price": 300, "category": "alcohol"}
        ]
        # 4 eligible → по-прежнему один бесплатный
        free_sum, free_names = apply_3plus1(items)
        self.assertEqual(free_sum, 50.0)


if __name__ == "__main__":
    unittest.main()
