"""Promotions that can be attached to products to discount their price."""
from abc import ABC, abstractmethod


class Promotion(ABC):
    """A named promotion; subclasses decide how the price is discounted."""

    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Promotion name must be a non-empty string.")
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """Return the discounted total price for buying quantity of product."""

    def get_name(self) -> str:
        """Return the promotion name."""
        return self.name

    def __str__(self):
        """Return the promotion name."""
        return self.name


class PercentDiscount(Promotion):
    """A fixed percentage off the whole purchase, e.g. 30% off."""

    def __init__(self, name: str, percent: float):
        super().__init__(name)
        if isinstance(percent, bool) or not isinstance(percent, (int, float)) \
                or not 0 <= percent <= 100:
            raise ValueError("Percent must be a number between 0 and 100.")
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """Return the full price reduced by percent."""
        return float(product.price * quantity * (100 - self.percent) / 100)


class SecondHalfPrice(Promotion):
    """Every second item costs half price."""

    def apply_promotion(self, product, quantity: int) -> float:
        """Charge full price for the odd items and half price for every second one."""
        half_price_items = quantity // 2
        full_price_items = quantity - half_price_items
        return float(product.price * full_price_items + product.price * 0.5 * half_price_items)


class ThirdOneFree(Promotion):
    """Buy 2, get 1 free: every third item costs nothing."""

    def apply_promotion(self, product, quantity: int) -> float:
        """Charge for all items except every third one."""
        free_items = quantity // 3
        return float(product.price * (quantity - free_items))
