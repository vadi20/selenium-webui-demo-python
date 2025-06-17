from utils.config import Config

def test_checkout_process(home_page):
    home_page.navigate_to_category('Laptops')
    product_page = home_page.select_product("Dell i7 8gb")
    product_page.add_to_cart()
    cart_page = home_page.go_to_cart()
    checkout_page = cart_page.place_order()
    checkout_page.fill_checkout_form(
        "John Doe", "USA", "NY", "4111111111111111", "12", "2025"
    )
    checkout_details = checkout_page.complete_purchase()
    assert "Thank you for your purchase" in checkout_details["message"]