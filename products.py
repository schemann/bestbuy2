"""Product model for the Best Buy store."""
from typing import List, Optional

from promotions import Promotion


class Product:
    """A product type available in the store, with its stock quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotions: List[Promotion] = []

    def get_quantity(self) -> int:
        """Return the quantity currently in stock."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """Set the stock quantity; a quantity of 0 deactivates the product."""
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def get_promotion(self) -> Optional[Promotion]:
        """Return the product's promotion, the first one if there are several, or None."""
        return self.promotions[0] if self.promotions else None

    def set_promotion(self, promotion: Optional[Promotion]):
        """Replace all promotions with this one; None removes every promotion."""
        if promotion is None:
            self.promotions = []
            return
        if not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion instance or None.")
        self.promotions = [promotion]

    def add_promotion(self, promotion: Promotion):
        """Bonus: add another promotion; the buyer gets the cheapest of them."""
        if not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion instance.")
        if promotion not in self.promotions:
            self.promotions.append(promotion)

    def remove_promotion(self, promotion: Promotion):
        """Remove one promotion from the product."""
        if promotion not in self.promotions:
            raise ValueError(f"{promotion} is not applied to {self.name}.")
        self.promotions.remove(promotion)

    def is_active(self) -> bool:
        """Return True if the product is active, otherwise False."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def promotion_text(self) -> str:
        """Return the promotion names for display, or 'None'."""
        if not self.promotions:
            return "None"
        return ", ".join(promotion.name for promotion in self.promotions)

    def show(self):
        """Print a one-line description of the product."""
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
              f"Promotion: {self.promotion_text()}")

    def total_price(self, quantity: int) -> float:
        """Return the price for quantity items, using the cheapest promotion if any."""
        if not self.promotions:
            return float(self.price * quantity)
        return min(promotion.apply_promotion(self, quantity) for promotion in self.promotions)

    def validate_purchase(self, quantity: int):
        """Raise ValueError unless this quantity can be bought right now."""
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Purchase quantity must be a positive integer.")
        if not self.active:
            raise ValueError(f"{self.name} is not active and cannot be bought.")
        if quantity > self.quantity:
            raise ValueError(
                f"Only {self.quantity} of {self.name} in stock, "
                f"cannot buy {quantity}."
            )

    def buy(self, quantity: int) -> float:
        """Buy the given quantity, update the stock and return the total price."""
        self.validate_purchase(quantity)
        self.set_quantity(self.quantity - quantity)
        return self.total_price(quantity)


class NonStockedProduct(Product):
    """A product without physical stock, e.g. a software license.

    Its quantity is always 0, and it can be bought in any amount.
    """

    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        """Refuse any quantity but 0: non-stocked products keep no stock."""
        if quantity != 0:
            raise ValueError(f"{self.name} is not stocked, its quantity stays 0.")

    def validate_purchase(self, quantity: int):
        """Check the quantity and active state; there is no stock to run out of."""
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Purchase quantity must be a positive integer.")
        if not self.active:
            raise ValueError(f"{self.name} is not active and cannot be bought.")

    def buy(self, quantity: int) -> float:
        """Return the total price without touching the (non-existent) stock."""
        self.validate_purchase(quantity)
        return self.total_price(quantity)

    def show(self):
        """Print the product with an unlimited quantity."""
        print(f"{self.name}, Price: ${self.price}, Quantity: Unlimited, "
              f"Promotion: {self.promotion_text()}")


class LimitedProduct(Product):
    """A product that can be bought at most `maximum` times per order, e.g. shipping."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            raise ValueError("Maximum must be a positive integer.")
        self.maximum = maximum

    def validate_purchase(self, quantity: int):
        """Refuse orders above the per-order maximum, then apply the normal checks."""
        super().validate_purchase(quantity)
        if quantity > self.maximum:
            raise ValueError(
                f"Only {self.maximum} of {self.name} allowed per order, "
                f"cannot buy {quantity}."
            )

    def show(self):
        """Print the product with its per-order limit."""
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
              f"Limited to {self.maximum} per order!, Promotion: {self.promotion_text()}")


def main():
    """Exercise the Product class with the example from the assignment."""
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()


if __name__ == "__main__":
    main()
