def test_product_details(home_page):
    home_page.navigate_to_category("Phones")
    product_page = home_page.select_product("Samsung galaxy s6")
    assert product_page.get_product_name() == "Samsung galaxy s6"
    assert "$" in product_page.get_product_price()

def test_add_to_cart(home_page):
    product_page = home_page.select_product("Nexus 6")
    alert_text = product_page.add_to_cart()
     
    assert "Product added" in alert_text