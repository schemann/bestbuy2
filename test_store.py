"""Unit tests for properties and magic methods (bonus step) and the Store."""
import pytest

from products import LimitedProduct, Product
from store import Store


@pytest.fixture(name="items")
def fixture_items():
    """The three products from the bonus example."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)
    return mac, bose, pixel


def test_negative_price_via_property_raises(items):
    """mac.price = -100 is refused and the price stays."""
    mac, _, _ = items
    with pytest.raises(ValueError):
        mac.price = -100
    assert mac.price == 1450


def test_str(items):
    """print(product) shows name, price, quantity and promotion."""
    mac, _, pixel = items
    assert str(mac) == "MacBook Air M2, Price: $1450, Quantity: 100, Promotion: None"
    assert "Limited to 1 per order!" in str(pixel)


def test_compare_prices(items):
    """> and < compare products by price."""
    mac, bose, pixel = items
    assert mac > bose
    assert bose < pixel
    assert not mac < bose


def test_in_store(items):
    """`in` checks whether a product is in the store."""
    mac, bose, pixel = items
    best_buy = Store([mac, bose])
    assert mac in best_buy
    assert pixel not in best_buy


def test_add_stores(items):
    """store + store gives a new store with the products of both, each once."""
    mac, bose, pixel = items
    first = Store([mac, bose])
    second = Store([bose, pixel])
    combined = first + second
    assert isinstance(combined, Store)
    assert combined.products == [mac, bose, pixel]
    assert first.products == [mac, bose]


def test_order_is_all_or_nothing(items):
    """A failing line leaves every stock untouched."""
    mac, _, pixel = items
    best_buy = Store([mac, pixel])
    with pytest.raises(ValueError):
        best_buy.order([(mac, 2), (pixel, 2)])
    assert mac.quantity == 100
    assert pixel.quantity == 250
