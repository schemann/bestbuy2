"""Product model for the Best Buy store."""
from typing import List, Optional

from promotions import Promotion


def _check_non_negative_int(value, label: str):
    """Raise ValueError unless value is an int >= 0 (bool is rejected)."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer.")


class Product:
    """A product type available in the store, with its stock quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        self.name = name
        self._price = 0.0
        self._quantity = 0
        self._active = True
        self._promotions: List[Promotion] = []
        self.price = price
        _check_non_negative_int(quantity, "Quantity")
        self._quantity = quantity

    @property
    def price(self) -> float:
        """The price of one item."""
        return self._price

    @price.setter
    def price(self, price: float):
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = price

    @property
    def quantity(self) -> int:
        """The quantity in stock; setting it to 0 deactivates the product."""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        _check_non_negative_int(quantity, "Quantity")
        self._quantity = quantity
        if quantity == 0:
            self.deactivate()

    @property
    def active(self) -> bool:
        """True if the product can be bought; change it with activate()/deactivate()."""
        return self._active

    def activate(self):
        """Activate the product."""
        self._active = True

    def deactivate(self):
        """Deactivate the product."""
        self._active = False

    @property
    def promotion(self) -> Optional[Promotion]:
        """The product's promotion (the first one if there are several), or None.

        Setting it replaces all promotions; setting None removes every promotion.
        """
        return self._promotions[0] if self._promotions else None

    @promotion.setter
    def promotion(self, promotion: Optional[Promotion]):
        if promotion is None:
            self._promotions = []
            return
        if not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion instance or None.")
        self._promotions = [promotion]

    @property
    def promotions(self) -> List[Promotion]:
        """A copy of all promotions applied to the product."""
        return list(self._promotions)

    def add_promotion(self, promotion: Promotion):
        """Bonus: add another promotion; the buyer gets the cheapest of them."""
        if not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion instance.")
        if promotion not in self._promotions:
            self._promotions.append(promotion)

    def remove_promotion(self, promotion: Promotion):
        """Remove one promotion from the product."""
        if promotion not in self._promotions:
            raise ValueError(f"{promotion} is not applied to {self.name}.")
        self._promotions.remove(promotion)

    def promotion_text(self) -> str:
        """Return the promotion names for display, or 'None'."""
        if not self._promotions:
            return "None"
        return ", ".join(promotion.name for promotion in self._promotions)

    def __str__(self):
        """Return a one-line description of the product."""
        return (f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
                f"Promotion: {self.promotion_text()}")

    def __lt__(self, other):
        """Compare products by price."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __gt__(self, other):
        """Compare products by price."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def total_price(self, quantity: int) -> float:
        """Return the price for quantity items, using the cheapest promotion if any."""
        if not self._promotions:
            return float(self.price * quantity)
        return min(promotion.apply_promotion(self, quantity) for promotion in self._promotions)

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
        self.quantity -= quantity
        return self.total_price(quantity)


class NonStockedProduct(Product):
    """A product without physical stock, e.g. a software license.

    Its quantity is always 0, and it can be bought in any amount.
    """

    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    @property
    def quantity(self) -> int:
        """Always 0: non-stocked products keep no stock."""
        return 0

    @quantity.setter
    def quantity(self, quantity: int):
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

    def __str__(self):
        """Return the product with an unlimited quantity."""
        return (f"{self.name}, Price: ${self.price}, Quantity: Unlimited, "
                f"Promotion: {self.promotion_text()}")


class LimitedProduct(Product):
    """A product that can be bought at most `maximum` times per order, e.g. shipping."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self._maximum = 1
        self.maximum = maximum

    @property
    def maximum(self) -> int:
        """The most items one order may contain."""
        return self._maximum

    @maximum.setter
    def maximum(self, maximum: int):
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            raise ValueError("Maximum must be a positive integer.")
        self._maximum = maximum

    def validate_purchase(self, quantity: int):
        """Refuse orders above the per-order maximum, then apply the normal checks."""
        super().validate_purchase(quantity)
        if quantity > self.maximum:
            raise ValueError(
                f"Only {self.maximum} of {self.name} allowed per order, "
                f"cannot buy {quantity}."
            )

    def __str__(self):
        """Return the product with its per-order limit."""
        return (f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
                f"Limited to {self.maximum} per order!, Promotion: {self.promotion_text()}")


def main():
    """Exercise the Product class with the example from the assignment."""
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.active)

    print(bose)
    print(mac)

    bose.quantity = 1000
    print(bose)


if __name__ == "__main__":
    main()
