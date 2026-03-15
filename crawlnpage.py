from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://www.coursera.org"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

course_urls = set()

# số page muốn crawl
total_pages = 40

for page in range(1, total_pages + 1):

    search_url = f"https://www.coursera.org/search?query=Personal%20Development&topic=Personal%20Development&page={page}"

    print("Đang crawl page:", page)

    driver.get(search_url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if (
            href.startswith("/learn/")
            or href.startswith("/specializations/")
            or href.startswith("/professional-certificates/")
        ):
            full_url = base_url + href
            course_urls.add(full_url)

driver.quit()

course_urls = list(course_urls)

print("Tổng số khóa học tìm được:", len(course_urls))

df = pd.DataFrame(course_urls, columns=["course_url"])
df.to_csv("coursera_course_urls.csv", index=False)

print("Đã lưu file coursera_course_urls.csv")