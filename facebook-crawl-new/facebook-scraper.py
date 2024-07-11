from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import re
def initDriver():
    CHROMEDRIVER_PATH = 'D:\App\chromedriver-win64\chromedriver.exe'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver

def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "pass")
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.submit()
    time.sleep(5)  # Đợi cho trang tải xong

def scrape_group_posts(driver, group_url):
    driver.get(group_url)
    time.sleep(5)  # Wait for the page to load

    posts = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load

        # Find post elements
        post_elements = driver.find_elements(By.XPATH, "//div[@role='article']")

        for post in post_elements:
            try:
                # Extract post ID from the link
                link_element = post.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
                href = link_element.get_attribute('href')
                post_id = re.search(r'/posts/(\d+)', href).group(1)

                # Extract post content
                content_element = post.find_element(By.XPATH, ".//div[contains(@class, 'x11i5rnm')]")
                content = content_element.text

                posts.append({"id": post_id, "content": content})
            except Exception as e:
                print(f"Error extracting post: {e}")

        # Check if we've reached the end of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return posts

def main():
    email = "anhduong080522@gmail.com"
    password = "minhmm"
    group_url = "https://www.facebook.com/groups/640812213243071"

    driver = initDriver()

    try:
        login_to_facebook(driver, email, password)
        posts = scrape_group_posts(driver, group_url)
        
        for post in posts:
            print(f"Author: {post['author']}")
            print(f"Content: {post['content']}")
            print("---")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()