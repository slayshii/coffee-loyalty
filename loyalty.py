DISCOUNT_RATES = {
    "Bronze": 0.05,
    "Silver": 0.10,
    "Gold": 0.15,
    "None": 0.0,
}

DEFAULT_LEVEL = "None"
ALCOHOL_CATEGORY = "alcohol"
DRINKS_FOR_FREE = 4
ROUND_DIGITS = 2


def apply_3plus1(items):
    #Акция '3+1': каждый 4-й напиток (не алкоголь) бесплатный.
    eligible = [i for i in items if i["category"] != ALCOHOL_CATEGORY]
    free_count = len(eligible) // DRINKS_FOR_FREE
    if free_count == 0:
        return 0.0, []

    cheapest = sorted(eligible, key=lambda i: i["price"])[:free_count]
    free_sum = round(sum(i["price"] for i in cheapest), ROUND_DIGITS)
    free_names = [i["name"] for i in cheapest]
    return free_sum, free_names


def apply_loyalty_discount(items, card_level):
    #Итоговая стоимость заказа с учётом акции 3+1 и скидки по карте.
    level = card_level if card_level in DISCOUNT_RATES else DEFAULT_LEVEL
    bonuses = []

    # Акция 3+1
    free_sum, free_names = apply_3plus1(items)
    if free_names:
        bonuses.append(f"3+1: бесплатно {', '.join(free_names)}")

    #Скидка по карте от суммы после акции
    base = sum(i["price"] for i in items) - free_sum
    discount = round(base * DISCOUNT_RATES[level], ROUND_DIGITS)
    if level != DEFAULT_LEVEL:
        bonuses.append(f"Скидка {level} {DISCOUNT_RATES[level]:.0%}")

    #Итог не может быть отрицательным
    total = max(round(base - discount, ROUND_DIGITS), 0.0)

    return {"total": total, "discount": discount, "bonuses": bonuses}


if __name__ == "__main__":
    order = [
        {"name": "Латте", "price": 250, "category": "coffee"},
        {"name": "Капучино", "price": 220, "category": "coffee"},
        {"name": "Эспрессо", "price": 150, "category": "coffee"},
        {"name": "Американо", "price": 120, "category": "coffee"},
        {"name": "Глинтвейн", "price": 300, "category": "alcohol"},
    ]

    for level in ("Silver", "Gold", "None"):
        print(level, "->", apply_loyalty_discount(order, level))
