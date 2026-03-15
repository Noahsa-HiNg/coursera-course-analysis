from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import os   # thêm dòng này

# đọc danh sách URL khóa học
df_urls = pd.read_csv("coursera_course_urls.csv")
course_urls = df_urls["course_url"].tolist()

# Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# tắt load image để tăng tốc
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

data = []

for i, url in enumerate(course_urls):

    print(f"Crawling {i+1}/{len(course_urls)}")

    # restart driver mỗi 100 course
    if i % 100 == 0 and i != 0:
        driver.quit()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    success = False

    # retry 3 lần nếu lỗi
    for attempt in range(3):

        try:
            driver.set_page_load_timeout(30)
            driver.get(url)
            success = True
            break

        except:
            print(f"Retry {attempt+1} for {url}")
            time.sleep(5)

    if not success:
        print("Skip:", url)
        continue

    time.sleep(random.uniform(3,6))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # --------------------
    # 1. Title
    # --------------------
    title = ""
    title_tag = soup.find("h1", {"data-e2e": "hero-title"})
    if title_tag:
        title = title_tag.get_text(strip=True)

    # --------------------
    # 2. Partner
    # --------------------
    partner = ""
    partner_img = soup.find("img", alt=True)
    if partner_img:
        partner = partner_img["alt"]

    # --------------------
    # 3. Enrollment
    # --------------------
    enroll = ""

    for p in soup.find_all("p", class_="css-4s48ix"):
        text = p.get_text()

        if "enrolled" in text:
            match = re.search(r"[\d,]+", text)
            if match:
                enroll = match.group()
                break

    # --------------------
    # 4. Rating
    # --------------------
    rating = ""
    rating_tag = soup.find("div", {"aria-roledescription": "rating"})
    if rating_tag:
        rating = rating_tag.get_text(strip=True)

    # --------------------
    # 5. Level
    # --------------------
    level = ""
    level_tag = soup.find("div", string=re.compile("level"))
    if level_tag:
        level = level_tag.get_text(strip=True)

    # --------------------
    # 6. Duration
    # --------------------
    duration = ""
    duration_tag = soup.find("div", string=re.compile("month|week"))
    if duration_tag:
        duration = duration_tag.get_text(strip=True)

    # --------------------
    # 7. Skills
    # --------------------
    skills = []
    skill_section = soup.find("ul", {"data-testid": "skills-section"})
    if skill_section:
        skill_links = skill_section.find_all("a")
        for s in skill_links:
            skills.append(s.get_text(strip=True))

    skills_text = ", ".join(skills)

    # --------------------
    # 8. Reviews
    # --------------------
    reviews = ""
    review_tag = soup.find("p", class_="css-vac8rf")
    if review_tag:
        text = review_tag.get_text()
        reviews = re.findall(r"[\d,]+", text)
        reviews = reviews[0] if reviews else ""

    data.append({
        "url": url,
        "title": title,
        "partner": partner,
        "enroll": enroll,
        "rating": rating,
        "level": level,
        "duration": duration,
        "skills": skills_text,
        "reviews": reviews
    })

driver.quit()

df = pd.DataFrame(data)

# --------------------
# tạo tên file tự tăng
# --------------------
base_name = "coursera_courses_dataset"
file_index = 1

while os.path.exists(f"{base_name}_{file_index}.csv"):
    file_index += 1

filename = f"{base_name}_{file_index}.csv"

df.to_csv(filename, index=False)

print(f"Dataset saved: {filename}")