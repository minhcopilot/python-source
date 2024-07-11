from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def initDriver():
    CHROMEDRIVER_PATH = 'D:\App\chromedriver-win64\chromedriver.exe'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu')
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
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    return driver

def login(driver, username, password):
    driver.get("https://www.facebook.com")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Facebook']")))

def scroll_page(driver, scroll_times, wait_time=2):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)
        
def scrape_group_posts(driver, group_url, posts_per_iteration=5, iterations=3):
    all_posts = set()  # Để lưu trữ tất cả các bài viết duy nhất

    for iteration in range(iterations):
        print(f"Iteration {iteration + 1}/{iterations}")
        driver.get(group_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='article']")))
        
        posts_in_current_iteration = 0
        while posts_in_current_iteration < posts_per_iteration:
            scroll_page(driver, 1)  # Cuộn một lần
            posts = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
            
            for post in posts:
                if posts_in_current_iteration >= posts_per_iteration:
                    break
                try:
                    content = post.find_element(By.CSS_SELECTOR, "div[data-ad-preview='message']").text
                    if content and content not in all_posts:
                        all_posts.add(content)
                        print(f"Post {posts_in_current_iteration + 1}:")
                        print(content)
                        print("---")
                        posts_in_current_iteration += 1
                except:
                    pass
        
        print(f"Collected {posts_in_current_iteration} posts in this iteration")
        if iteration < iterations - 1:
            print("Waiting 5 seconds before next iteration...")
            time.sleep(5)  

    print(f"Total unique posts collected: {len(all_posts)}")

def main():
    driver = initDriver()

    username = "anhduong080522@gmail.com"
    password = "minhmm"
    group_url = "https://www.facebook.com/groups/1390167227872503/?sorting_setting=CHRONOLOGICAL"

    try:
        login(driver, username, password)
        scrape_group_posts(driver, group_url, posts_per_iteration=5, iterations=3)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()