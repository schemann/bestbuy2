"""Unit tests for the Product class."""
import pytest

from products import LimitedProduct, NonStockedProduct, Product


def test_create_normal_product():
    """A product with valid details stores them and starts active."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active()


def test_create_product_with_empty_name_raises():
    """An empty name is rejected."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_with_negative_price_raises():
    """A negative price is rejected."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity():
    """Buying the whole stock leaves the product at 0 and inactive."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.buy(100)
    assert product.get_quantity() == 0
    assert not product.is_active()


def test_set_quantity_to_zero_deactivates_product():
    """Setting the quantity to 0 directly also deactivates the product."""
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    product.set_quantity(0)
    assert not product.is_active()


def test_buy_modifies_quantity_and_returns_total_price():
    """A purchase lowers the stock and returns quantity times price."""
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    total = product.buy(50)
    assert total == 12500
    assert product.get_quantity() == 450
    assert product.is_active()


def test_buy_more_than_in_stock_raises():
    """Buying more than the stock raises and leaves the stock unchanged."""
    product = Product("Google Pixel 7", price=500, quantity=250)
    with pytest.raises(ValueError):
        product.buy(251)
    assert product.get_quantity() == 250


def test_non_stocked_product_has_zero_quantity_and_stays_active():
    """A non-stocked product starts at 0, stays active and keeps 0 after a purchase."""
    product = NonStockedProduct("Windows License", price=125)
    assert product.get_quantity() == 0
    assert product.is_active()
    assert product.buy(3) == 375
    assert product.get_quantity() == 0
    assert product.is_active()


def test_non_stocked_product_refuses_stock():
    """Setting a quantity on a non-stocked product raises."""
    product = NonStockedProduct("Windows License", price=125)
    with pytest.raises(ValueError):
        product.set_quantity(10)


def test_limited_product_refuses_more_than_maximum():
    """Buying more than the per-order maximum raises and keeps the stock."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(ValueError):
        product.buy(2)
    assert product.get_quantity() == 250
    assert product.buy(1) == 10
    assert product.get_quantity() == 249
