import requests
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # headless version


# Options are for headless browser. Can emulate mobile browser too, etc.
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


url: str = "https://www.amazon.com/gp/product/B088MYGMPJ?pf_rd_r=JX5ZMYW0RXG6K7BRQZ85&pf_rd_p=edaba0ee-c2fe-4124-9f5d-b31d6b1bfbee"
title_selector: str = "#productTitle"
price_selector: str = "#priceblock_ourprice"

# r = requests.get(url)
# html_str: str = r.text
# print(html_str)  # Cannot use requests with Amazon! Need selenium instead

# Use selenium headless browser to get HTML
driver.get(url)
body_el = driver.find_element_by_css_selector("body")
body_html_str: str = body_el.get_attribute("innerHTML")
# print(body_html_str)

# Can still use requests_html HTML class to scrape the html
html_obj = HTML(html=body_html_str)
product_title: str = html_obj.find(
    selector=title_selector, first=True
).text  # first=True for only one
product_price: str = html_obj.find(
    selector=price_selector, first=True
).text  # first=True for only one
# print(product_title)  # Paper Mario: The Origami King - Nintendo Switch
# print(product_price)  # $59.99
