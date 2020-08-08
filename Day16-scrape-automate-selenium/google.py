import time
from selenium import webdriver

"""
NOTES: - GET a url and then need to find <input type='text' /> for input box For our purposes it's: <input name="q" type="text"/>
    - HTML 'name' attribute comes/relies on backend so harder to change than
      'class' or 'id' attributes. 'name' is how it functions (not its look)
    - Use webdriver.find_element_by_name() to find name='q'
    - Use search_element.send_keys("selenium python")
    - Submit search by finding <input type='submit'/>, <button type='submit'/>
    - The type='submit' WILL override the 'name' attr for submit buttons.
      This is different from input boxes.
    - Use find_element_by_css_selector("input[type='submit']")
    - Use submit_button_element.click() to submit query
    - Use getpass library for secure password storage
    - Use requests-html to scrape homepage (r.html.links, r.html.find(), etc.)
    - Use browser.find_elements_by_xpath for advanced css_selector replacement
    - Can pass browser session as arg to a function click_to_follow(browser)
    - Use post_xpath: str = "//a[contains(@href, '/p/')]" for finding <a> tags
    - Can use from urllib.parse import urlparse to parse URL into 6 parts
    - Need to use 'wb' (write bytes) to save images and videos
    - Use PIL to verify the size of any given image. If a size doesn't meet
      criteria you could save empty file (no data) so it is skipped in future
      runs (if os.path.exists: continue).
    - Could add a parent dir for each user with its own /data sub-directory
    - LONG TERM GOAL: Use ML to classify post's image/video and then comment
      in a relevant fashion.
    - Cannot element.click() an SVG need parent element. You can chain the
      find_elements_by...() methods: parent=el.find_element_by_xpath('..')
"""

"""
HTML from <input type='text'> on Google.com:

<input class="gLFyf gsfi" maxlength="2048" name="q" type="text" jsaction="paste:puy29d" aria-autocomplete="both" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" autofocus="" role="combobox" spellcheck="false" title="Search" value="" aria-label="Search" data-ved="0ahUKEwiV9vSqq-zqAhVSLX0KHU6TCF0Q39UDCAY">

"""

browser = webdriver.Chrome()

url: str = "https://google.com"
browser.get(url)

search_element = browser.find_element_by_name("q")
# search_element = browser.find_element_by_css_selector("input[name='q']")
# print(
#     search_element
# )  # <selenium.webdriver.remote.webelement.WebElement (session="d0fbb4f2e40bdc70c205e8ae5aa25cdc", element="96460394-bfa3-4cc5-87dc-24b9b757c481")>

time.sleep(2)
search_element.send_keys("selenium python")
# Then need to find a way to submit the form using either:
# <input type='submit'/> or <button type='submit'/> or <form>
submit_button_element = browser.find_element_by_css_selector(
    "input[type='submit']"
)
# print(
#     type(submit_button_element)
# )  # <class 'selenium.webdriver.remote.webelement.WebElement'>
# print(submit_button_element.get_attribute("name"))  # btnK
time.sleep(2)
submit_button_element.click()
