import time
import requests
import typing as t
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # headless version

"""
NOTES:
    - Don't hardcode URL patterns; first find the pattern and piece together
    -
"""
# Options are for headless browser. Can emulate mobile browser too, etc.
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

categories: t.List[str] = [
    "https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/",
    "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/",
    "https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/",
]

first_url: str = categories[0]
driver.get(first_url)
body_el = driver.find_element_by_css_selector("body")
body_html_str: str = body_el.get_attribute("innerHTML")

# Convert to HTML instance. The .links attr shows all links in html
html_obj = HTML(html=body_html_str)

# Modify links list to have '/' at beginning. Just trims list a little.
new_links: t.List[str] = [x for x in html_obj.links if x.startswith("/")]
# print(new_links)
# ['/product-reviews/B085M812NM/ref=zg_bs_p...', '/gcx/Gifts-for-Everyone/gfhz/
# Get rid of 'product-reviews/' URLs:
new_links: t.List[str] = [x for x in new_links if "product-reviews/" not in x]

# Now with a leaner list of links, let's make our product page links list
product_page_links: t.List[str] = [f"https://amazon.com{x}" for x in new_links]
first_product_link: str = product_page_links[0]
# print(first_product_link)
# https://amazon.com/product-reviews/B07TMJ8S5Z/ref=zg_bs_pc_cr_1/130-9341...

# Let's refactor by turning into a function
def scrape_product_page(
    url: str,
    title_selector: str = "#productTitle",
    price_selector: str = "#priceblock_ourprice",
):
    driver.get(url)
    time.sleep(2)

    # Fetch body HTML so we can parse it
    body_el = driver.find_element_by_css_selector("body")
    body_html_str: str = body_el.get_attribute("innerHTML")

    # Convert to HTML instance. The .links attr shows all links in html
    html_obj = HTML(html=body_html_str)

    # Now that we have product page links, we can scrape the titles and prices
    product_title: str = html_obj.find(
        selector=title_selector, first=True
    ).text  # first=True for only one
    product_price: str = html_obj.find(
        selector=price_selector, first=True
    ).text  # first=True for only one

    return product_title, product_price


# Loop through product page links and skip w/ try/except if not a product page
for link in product_page_links:
    title: t.Optional[str] = None
    price: t.Optional[str] = None
    try:
        title, price = scrape_product_page(link)
    except AttributeError:
        # AttributeError: NoneType has no 'text'
        pass
    if title is not None and price is not None:
        print(link, title, price)
"""
    https://amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08636NKF8/ref=zg_bs_pc_23/132-2947938-2062417?_encoding=UTF8&psc=1&refRID=7GCSVC
    TFH75FDKJJA2K8 Apple MacBook Air (13-inch, 8GB RAM, 256GB SSD Storage) - Gold (Latest Model) $899.00

    https://amazon.com/TP-Link-AC1200-WiFi-Router-Access/dp/B07RKYQGG4/ref=zg_bs_pc_45/132-2947938-2062417?_encoding=UTF8&psc=1&refRID=7GCSVCTF
    H75FDKJJA2K8 TP-Link AC1200 WiFi Router - Dual Band Wireless Internet Router, 4 x 10/100 Mbps Fast Ethernet Ports, Supports Guest WiFi, Acc
    ess Point Mode, IPv6 and Parental Controls(Archer A5) $29.99

    https://amazon.com/Charger-Magsafe-Adapter-Compatible-MacBook/dp/B07YD1LZ87/ref=zg_bs_pc_18/132-2947938-2062417?_encoding=UTF8&psc=1&refRID
    =7GCSVCTFH75FDKJJA2K8 Mac Book Pro Charger, 60W Magsafe 2 T-tip Power Adapter Charger Compatible with MacBook Charger/Mac Book Air（ After
    Late 2012） $22.99
"""
scrape_product_page(first_product_link)
