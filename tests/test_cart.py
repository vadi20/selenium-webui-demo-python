def test_remove_from_cart(home_page):
    home_page.navigate_to_category("Laptops")
    product_page = home_page.select_product("MacBook air")
    product_page.add_to_cart()
    cart_page = home_page.go_to_cart()
    cart_page.delete_item()
    assert cart_page.get_cart_items()["count"] == 0

def test_place_order(home_page):
    home_page.navigate_to_category("Monitors")
    product_page = home_page.select_product("ASUS Full HD")
    product_page.add_to_cart()
    cart_page = home_page.go_to_cart()
    cart_page.place_order()
    assert cart_page.is_displayed(cart_page.PLACE_ORDER_BTN)