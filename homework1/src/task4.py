def calculate_discount(price, discount):
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")

    return price - (price * (discount / 100))
    