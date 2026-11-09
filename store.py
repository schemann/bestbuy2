"""Store that holds products and processes orders."""

from typing import List, Tuple

import products


class Store:
    """A store that holds products and processes multi-product orders."""

    def __init__(self, product_list: List[products.Product]):
        self.products = []
        for product in product_list:
            self.add_product(product)

    def add_product(self, product: products.Product):
        """Add a product to the store."""
        if not isinstance(product, products.Product):
            raise TypeError("Only Product instances can be added to the store.")
        if product in self.products:
            raise ValueError(f"{product.name} is already in the store.")
        self.products.append(product)

    def remove_product(self, product: products.Product):
        """Remove a product from the store."""
        if product not in self.products:
            raise ValueError("Product is not in the store.")
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total number of items in the store."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> List[products.Product]:
        """Return all active products in the store."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """Buy every (product, quantity) pair and return the total price.

        The whole order is validated before anything is bought, so a failing
        line never leaves the store with a partially processed order.
        """
        requested = {}
        for item in shopping_list:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("Each order item must be a (product, quantity) tuple.")
            product, quantity = item
            if product not in self.products:
                raise ValueError("Ordered product is not in the store.")
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Order quantity must be a positive integer.")
            requested[product] = requested.get(product, 0) + quantity

        for product, quantity in requested.items():
            product.validate_purchase(quantity)

        total_price = 0.0
        for product, quantity in requested.items():
            total_price += product.buy(quantity)
        return total_price


def main():
    """Exercise the Store class with the example from the assignment."""
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.NonStockedProduct("Windows License", price=125),
                    ]

    best_buy = Store(product_list)
    active_products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(active_products[0], 1), (active_products[1], 2)]))


if __name__ == "__main__":
    main()
