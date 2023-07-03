from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def add_to_cart(browser, price):
    """adds the products to the cart and return number of items added"""
    for amount in price:
        browser.find_element(By.XPATH,f"//*[contains(text(),'{amount}')]"
                                     f"/following-sibling::button").click()
    cart_item =browser.find_element(By.ID,"cart").text
    if cart_item == "1 item":
        print("Added 1 items, redirecting to cart")
    else:
        print("Kindly add 1 items to proceed to cart")

def get_product(temp):
    product = ""
    items = list()
    if temp <= 30:
        product = "moisturizer" 
        items = ["Almond"]
    elif temp >= 30:
        product = "sunscreen"
        items = ["SPF-30"]
    return product,items

def get_temperature(browser):
    """returns the temperature on the landing page"""
    temperature = browser.find_element(By.ID,"temperature")
    return int(temperature.text[:-2])
    

def click_on_buy(browser, product):
    """go to product page based on the temperature value"""
    browser.find_element(By.XPATH,f"//button[contains(.,'Buy {product}s')]").click()


def take_me_to_product_page(browser):
    """takes from landing page to product page"""
    temperature = get_temperature(browser)
    product,items = get_product(temperature)
    click_on_buy(browser, product)
    return items

def min_price(browser, items):
    """Returns the price of the least expensive aloe and almond products"""
    price = list()
    for item in items:
        item_list = browser.find_elements(By.XPATH,f"//*[contains(text(),'{item}') or "
                                                  f"contains(text(),'{item.lower()}')]"
                                                  f"/following-sibling::p")
        price_list = [item_list[i-1].text for i in range(len(item_list))]
        price_only = [price[-3:] for price in price_list]
        price.append(int(min(price_only)))
    return price

def take_me_to_cart(browser):
    """takes from landing page to cart page"""
    items = take_me_to_product_page(browser)
    cheap_products = min_price(browser, items)
    add_to_cart(browser, cheap_products)
    click_on_cart(browser)
    return cheap_products

def click_on_cart(browser):
    """go to cart page"""
    browser.find_element(By.ID,"cart").click()

def cart_page():
    browser = webdriver.Chrome()
    # navigate to main page
    browser.get("https://weathershopper.pythonanywhere.com/")
    items = take_me_to_product_page(browser)
    time.sleep(3)
    cheap_products = min_price(browser,items)
    # add them to cart
    add_to_cart(browser,cheap_products)
    # go to cart
    click_on_cart(browser)
    time.sleep(100)
    browser.quit()
if __name__ == "__main__":
    cart_page()