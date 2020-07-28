import os
import time
import requests
import typing as t
from selenium import webdriver
from urllib.parse import urlparse
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

time.sleep(2)
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
# time.sleep(2)
# new_user_url: str = "https://www.instagram.com/rongalk"
# browser.get(new_user_url)
# time.sleep(2)
# click_to_follow(browser)


# ===== Scrape content from a user's post w/ XPATH =====
time.sleep(2)
the_rock_url: str = "https://www.instagram.com/therock"
browser.get(the_rock_url)

# Find the URL for any given post: <a href="/p/CDIQH2zlQXx/" tabindex="0">
time.sleep(5)
post_url_pattern: str = "https://www.instagram.com/p/<post-slug-id>"
post_xpath: str = "//a[contains(@href, '/p/')]"
post_links_elements: t.List = browser.find_elements_by_xpath(post_xpath)
post_link_el = None

if len(post_links_elements) > 0:
    post_link_el = post_links_elements[0]

if post_link_el is not None:
    time.sleep(5)
    post_link_href: str = post_link_el.get_attribute("href")
    browser.get(post_link_href)

# Extract/dl images and videos from post page save in images dir
video_elements: t.List = browser.find_elements_by_xpath("//video")
image_elements: t.List = browser.find_elements_by_xpath("//img")
# [<selenium.webdriver.remote.webelement.WebElement (session="c911e7312d...
# Create new 'images' directory
base_dir: str = os.path.dirname(os.path.abspath(__file__))
data_dir: str = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)


def scrape_and_save(elements: t.List):
    """
    Iterate through a list of image and/or video HTML elements
    and extract the image/video URL from each element. With this
    URL, parse it with urlparse().path and use this to create a
    new filepath. Then open a GET request and steam and save
    chunks of data to the unique filepath.

    Params:
        elements: t.List -- List of webdriver elements objects.
    """
    for el in elements:
        # Get the urls to all the images
        # print(el.get_attribute("src"))
        """
        https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/94194265_2959226834168352_8521584817458905088_n.
        jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_ohc=cIBSnUnifq4AX-hiNAH&oh=695b693aece7e53daa57902cd17c897e&oe=5
        F49F505
        """
        img_url: str = el.get_attribute("src")
        base_url: str = urlparse(
            img_url
        ).path  # Also .params, .query, .fragment
        # print(f"base_url: {base_url}")
        filename: str = os.path.basename(base_url)
        # print(f"filename: {filename}")
        filepath: str = os.path.join(data_dir, filename)
        # print(f"filepath: {filepath}")

        # If file already saved/exists then skip
        if os.path.exists(filepath):
            continue

        # Make a GET request to the img_url and extract/save data
        with requests.get(img_url, stream=True) as r:
            try:
                r.raise_for_status()
            except:
                continue
            # Save data to the file
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        # print(f"Writing chunk: {chunk}")
                        f.write(chunk)


# Run scrape_and_save() for images and videos
# scrape_and_save(image_elements)
# scrape_and_save(video_elements)


"""
LONG TERM GOAL: Use ML to then classify post's image/video and reply
with a relevant comment.
"""

# ===== Add a comment on an individual post w/ XPATH =====
# Just need to load a user's post first
def automate_comment(browser, content: str = "Way to go!"):
    """
    Automatically add a comment to an individual post.

    Params:
        content: str -- Actual comment text string.
    """
    time.sleep(3)

    """
    <textarea aria-label="Add a comment…" placeholder="Add a comment…" class="Ypffh" autocomplete="off" autocorrect="off" style="height: 18px;"></textarea>
    """
    add_comment_xpath: str = "//textarea[contains(@placeholder, 'Add a comment')]"
    add_comment_el = browser.find_element_by_xpath(add_comment_xpath)
    print(add_comment_el)
    # add_comment_el.send_keys(content)

    # ===== Find 'Post' submit button after comment has been entered =====
    """
    <button class="sqdOP yWX7d    y3zKF     " type="submit">Post</button>
    """
    submit_btns_xpath: str = "button[type='submit']"
    submit_btns_elements: t.List = browser.find_elements_by_css_selector(
        submit_btns_xpath
    )

    # Click on all the submit buttons
    time.sleep(2)
    for btn in submit_btns_elements:
        try:
            btn.click()
        except:
            pass


# automate_comment(content="That's so cool!")


# ===== Automate clicking the 'Like' button =====
"""
<button class="wpO6b " type="button"><div class="QBdPU "><svg aria-label="Like" class="_8-yf5 " fill="#262626" height="24" viewBox="0 0 48 48" width="24"><path d="M34.6 6.1c5.7 0 10.4 5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg></div></button>
"""


def automate_like(browser):
    like_button_svg_xpath: str = "//*[contains(@aria-label, 'Like')]"
    # Or, "svg[aria-label='Like']"  # 'Like' toggles to 'Unlike'
    like_button_svg_els: t.List = browser.find_elements_by_xpath(
        like_button_svg_xpath
    )

    # Extract largest heart SVG based on "height" attribute
    max_like_button_svg_height: int = -1
    for el in like_button_svg_els:
        svg_height: t.Union[int, str] = el.get_attribute("height")
        if int(svg_height) > max_like_button_svg_height:
            max_like_button_svg_height = int(svg_height)

    # Alternative: Get list of el heights, convert to Set for just 1
    # Then identify/find that specific element to then click.

    # Click the tallest 'height' like button on the page
    # Iterate twice as sometimes Elements go 'stale'
    like_button_svg_els: t.List = browser.find_elements_by_xpath(
        like_button_svg_xpath
    )
    for el in like_button_svg_els:
        svg_height: t.Union[int, str] = el.get_attribute("height")
        if int(svg_height) == max_like_button_svg_height:
            # Chain find_elements_by methods:
            parent_button_el = el.find_element_by_xpath("..")
            time.sleep(2)
            try:
                parent_button_el.click()
            except:
                pass


# Call the automate_like() function
# automate_like(browser)
