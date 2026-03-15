from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://www.coursera.org"
search_url = "https://www.coursera.org/search?query=artificial%20intelligence&topic=Data%20Science&sortBy=BEST_MATCH"

# mở browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(search_url)

# đợi trang load
time.sleep(5)

# scroll để load thêm course
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# lấy html
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

course_urls = set()

# tìm tất cả thẻ a
for a in soup.find_all("a", href=True):

    href = a["href"]

    # lọc link course
    if (
        href.startswith("/learn/")
        or href.startswith("/specializations/")
        or href.startswith("/professional-certificates/")
    ):
        full_url = base_url + href
        course_urls.add(full_url)

driver.quit()

course_urls = list(course_urls)

print("Số khóa học tìm được:", len(course_urls))

# lưu file
df = pd.DataFrame(course_urls, columns=["course_url"])
df.to_csv("coursera_course_urls.csv", index=False)

print("Đã lưu file coursera_course_urls.csv")