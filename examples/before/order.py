from decimal import Decimal

TAX_RATE = Decimal("0.085")


def process_order(items, loyalty_multiplier=1.0):
    subtotal = sum(Decimal(item["price"]) * item.get("qty", 1) for item in items)
    taxed = subtotal + subtotal * TAX_RATE
    if loyalty_multiplier > 1.0:
        taxed *= Decimal(loyalty_multiplier)
    return taxed.quantize(Decimal("0.01"))
