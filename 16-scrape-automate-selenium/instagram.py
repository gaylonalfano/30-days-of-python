import time
import typing as t
from selenium import webdriver
import settings

# import getpass
# my_password = getpass.getpass(prompt="What's your password? ")
# print(my_password)

browser = webdriver.Chrome()

url: str = "https://www.instagram.com"
browser.get(url)

# ===== Log into account =====
time.sleep(2)
username_el = browser.find_element_by_name("username")
username_el.send_keys(settings.INSTA_USERNAME)

password_el = browser.find_element_by_name("password")
password_el.send_keys(settings.INSTA_PASSWORD)

time.sleep(1)
submit_btn_el = browser.find_element_by_css_selector("button[type='submit']")
submit_btn_el.click()


# ===== Scrape homepage HTML for parsing =====
# After logging in, can retrieve/scrape html of home page
# Can use requests-html for advanced scraping of links, etc.
time.sleep(6)
body_el = browser.find_element_by_css_selector("body")
body_html_text: str = body_el.get_attribute("innerHTML")

# ===== Auto click 'Follow' on a user's page using XPATH =====
# <button class="_5f5mN       jIbKX  _6VtSN     yZn4P   ">Follow</button>
# Hard to make sense of so can find all buttons or use xpath (advanced)
def click_to_follow(browser):
    """
    Use current browser/client session to click 'Follow' button.
    Params:
        browser: Selenium webdriver.Chrome() session
    """
    # browser.find_elements_by_css_selector("button")
    # my_button_xpath: str = "//button"
    # browser.find_elements_by_xpath(my_button_xpath)

    # <button>
    my_follow_btn_xpath: str = "//button[contains(text(), 'Follow')][not(contains(text(), 'Following'))]"
    follow_btn_elements: t.List = browser.find_elements_by_xpath(
        my_follow_btn_xpath
    )

    # <a>
    # my_follow_btn_xpath: str = "//a[contains(text(), 'Follow')][not(contains(text(), 'Following'))]"
    # follow_btn_elements: t.List = browser.find_elements_by_xpath(
    #     my_follow_btn_xpath
    # )

    # All elements
    # my_follow_btn_xpath: str = "//*[contains(text(), 'Follow')][not(contains(text(), 'Following'))][not(contains(text(), 'Followers'))]"
    # follow_btn_elements: t.List = browser.find_elements_by_xpath(
    #     my_follow_btn_xpath
    # )

    for btn in follow_btn_elements:
        # Attempt to click each follow button on the page
        time.sleep(2)  # self-throttle
        try:
            btn.click()
        except:
            pass


# ===== Navigate to the new user we want to follow =====
time.sleep(2)
new_user_url: str = "https://www.instagram.com/rongalk"
browser.get(new_user_url)
time.sleep(2)
click_to_follow(browser)
