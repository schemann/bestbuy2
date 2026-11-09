"""Interactive command-line menu for the Best Buy store."""

import products
import store


def print_product_list(product_list):
    """Print a numbered list of the given products."""
    print("------")
    for index, product in enumerate(product_list, 1):
        print(f"{index}. ", end="")
        product.show()
    print("------")


def show_products(shop):
    """Menu action: list all active products in the store."""
    print_product_list(shop.get_all_products())


def show_total_amount(shop):
    """Menu action: show the total number of items in the store."""
    print(f"Total of {shop.get_total_quantity()} items in store")


def make_order(shop):
    """Menu action: collect (product, quantity) pairs and place the order."""
    product_list = shop.get_all_products()
    print_product_list(product_list)
    shopping_list = []
    print("When you want to finish order, enter empty text.")

    while True:
        product_number = input("Which product # do you want? ").strip()
        amount = input("What amount do you want? ").strip()
        if not product_number or not amount:
            break
        try:
            index = int(product_number)
            quantity = int(amount)
            if not 1 <= index <= len(product_list) or quantity <= 0:
                raise ValueError
        except ValueError:
            print("Error adding product!\n")
            continue
        shopping_list.append((product_list[index - 1], quantity))
        print("Product added to list!\n")

    if not shopping_list:
        return
    try:
        total_price = shop.order(shopping_list)
    except ValueError as error:
        print(f"Error while making order! {error}")
        return
    print(f"********\nOrder made! Total payment: ${total_price}")


MENU = {
    1: ("List all products in store", show_products),
    2: ("Show total amount in store", show_total_amount),
    3: ("Make an order", make_order),
    4: ("Quit", None),
}


def print_menu():
    """Print the store menu."""
    print("\n   Store Menu\n   ----------")
    for number, (label, _) in MENU.items():
        print(f"{number}. {label}")


def get_menu_choice():
    """Show the menu until the user picks a valid option and return it."""
    while True:
        print_menu()
        try:
            choice = int(input("Please choose a number: "))
        except ValueError:
            choice = None
        if choice in MENU:
            return choice
        print("Error with your choice! Try again!")


def start(shop):
    """Run the interactive store menu for the given store until Quit."""
    while True:
        _, action = MENU[get_menu_choice()]
        if action is None:
            break
        action(shop)


def main():
    """Set up the initial inventory and start the store menu."""
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]
    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
