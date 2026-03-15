import requests

def get_first_seen_date(url):
    try:
        # Gọi API của Wayback Machine tìm bản lưu (snapshot) đầu tiên (limit=1)
        api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&limit=1&output=json&fl=timestamp"
        response = requests.get(api_url, timeout=10).json()
        
        # Lấy kết quả (Dạng chuỗi: YYYYMMDDhhmmss)
        if len(response) > 1:
            timestamp = response[1][0] 
            year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:8]
            return f"{year}-{month}-{day}"
    except:
        return None
    return None

# Ví dụ test thử:
url = "https://www.coursera.org/learn/film-documentaries-write-film--edit-short-a-documentary"
print("Ngày khóa học xuất hiện trên Internet:", get_first_seen_date(url))