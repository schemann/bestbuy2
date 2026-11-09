"""Unit tests for the promotions and their use in Product."""
import pytest

from products import NonStockedProduct, Product
from promotions import PercentDiscount, Promotion, SecondHalfPrice, ThirdOneFree


def test_promotion_is_abstract():
    """A general Promotion cannot be created."""
    with pytest.raises(TypeError):
        Promotion("General")  # pylint: disable=abstract-class-instantiated


def test_percent_discount():
    """30% off 2 items of 100 costs 140."""
    product = Product("Item", price=100, quantity=10)
    product.promotion = PercentDiscount("30% off!", percent=30)
    assert product.buy(2) == 140


def test_second_half_price():
    """3 items: two full price, one half price."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.promotion = SecondHalfPrice("Second Half price!")
    assert product.buy(3) == 1450 * 2 + 725
    assert product.quantity == 97


def test_third_one_free():
    """7 items: two of them are free."""
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    product.promotion = ThirdOneFree("Third One Free!")
    assert product.buy(7) == 250 * 5


def test_promotion_on_non_stocked_product():
    """Promotions also apply to products without stock."""
    product = NonStockedProduct("Windows License", price=125)
    product.promotion = PercentDiscount("30% off!", percent=30)
    assert product.buy(2) == 175


def test_set_get_and_remove_promotion():
    """The setter replaces, None removes, and the getter returns the current one."""
    product = Product("Item", price=100, quantity=10)
    assert product.promotion is None
    promotion = ThirdOneFree("Third One Free!")
    product.promotion = promotion
    assert product.promotion is promotion
    product.promotion = None
    assert product.promotion is None
    assert product.buy(3) == 300


def test_same_promotion_on_several_products():
    """One promotion object can be shared between products."""
    promotion = PercentDiscount("10% off", percent=10)
    first = Product("A", price=100, quantity=5)
    second = Product("B", price=50, quantity=5)
    first.promotion = promotion
    second.promotion = promotion
    assert first.buy(1) == 90
    assert second.buy(1) == 45


def test_multiple_promotions_give_the_cheapest_price():
    """Bonus: with several promotions the buyer pays the lowest price."""
    product = Product("Item", price=100, quantity=10)
    product.add_promotion(ThirdOneFree("Third One Free!"))
    product.add_promotion(PercentDiscount("50% off", percent=50))
    assert product.buy(3) == 150
    product.remove_promotion(product.promotion)
    assert product.buy(3) == 150
    assert product.promotion.name == "50% off"


def test_invalid_promotion_is_rejected():
    """Only Promotion objects or None can be set."""
    product = Product("Item", price=100, quantity=10)
    with pytest.raises(TypeError):
        product.promotion = "20% off"
