import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

def encode_coursera_data(df):
    df = df.copy()

    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    # ==========================================
    # BƯỚC MỚI BỔ SUNG: LÀM SẠCH CỘT SỐ 
    # ==========================================
    for col in ['enroll', 'reviews', 'rating']:
        if col in df.columns:
            cleaned_str = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(cleaned_str, errors='coerce')

    # ==========================================
    # 1. XỬ LÝ LEVEL
    # ==========================================
    level_mapping = {
        'Beginner level': 1, 
        'Intermediate level': 2, 
        'Advanced level': 3, 
        'Mixed level': 0
    }
    df['level_encoded'] = df['level'].map(level_mapping).fillna(0)
    df = df.drop(columns=['level'])

    # ==========================================
    # 2. XỬ LÝ DURATION (Dùng bản quy ra GIỜ)
    # ==========================================
    def duration_to_hours(text):
        text = str(text).lower() 
        if 'month' in text:
            if '3' in text and '6' in text:
                return 180.0  
            elif '1' in text and '3' in text:
                return 80.0   
            else:
                return 40.0   
        elif 'week' in text:
            if '1' in text and '4' in text:
                return 25.0   
            else:
                return 10.0   
        elif 'hour' in text:
            return 2.0        
        else:
            return 0.0        
            
    df['duration_hours'] = df['duration'].apply(duration_to_hours)
    df = df.drop(columns=['duration'])

    # ==========================================
    # 3. XỬ LÝ PARTNER
    # ==========================================
    top_20_partners = df['partner'].value_counts().nlargest(20).index
    df['partner_grouped'] = df['partner'].where(df['partner'].isin(top_20_partners), 'Other')
    df = pd.get_dummies(df, columns=['partner_grouped'], prefix='partner', drop_first=False)
    df = df.drop(columns=['partner'])

    # ==========================================
    # 4. XỬ LÝ CATEGORY
    # ==========================================
    if 'category' in df.columns:
        df = pd.get_dummies(df, columns=['category'], prefix='cat', drop_first=False)

    # ==========================================
    # 5. XỬ LÝ SKILLS
    # ==========================================
    df['skills'] = df['skills'].fillna('').astype(str).apply(
        lambda x: [s.strip() for s in x.split(',') if s.strip()]
    )
    mlb = MultiLabelBinarizer()
    skills_encoded = pd.DataFrame(
        mlb.fit_transform(df['skills']), 
        columns=[f"skill_{c}" for c in mlb.classes_], 
        index=df.index
    )
    top_50_skills = skills_encoded.sum().nlargest(50).index
    skills_encoded = skills_encoded[top_50_skills]
    df = pd.concat([df, skills_encoded], axis=1)
    df = df.drop(columns=['skills'])

    # ==========================================
    # 6. XỬ LÝ TITLE (ĐÃ KHÔI PHỤC LẠI)
    # ==========================================
    tfidf = TfidfVectorizer(max_features=20, stop_words='english')
    title_tfidf = tfidf.fit_transform(df['title'].fillna(''))
    title_encoded = pd.DataFrame(
        title_tfidf.toarray(), 
        columns=[f"title_{w}" for w in tfidf.get_feature_names_out()], 
        index=df.index
    )
    df = pd.concat([df, title_encoded], axis=1)
    df = df.drop(columns=['title'])

    # ==========================================
    # 7. ÉP KIỂU BOOLEAN -> INT
    # ==========================================
    boolean_cols = df.select_dtypes(include='bool').columns
    df[boolean_cols] = df[boolean_cols].astype(int)

    return df

# Cách gọi hàm:
data_path = r"E:\University\semeter6\coursera-analy\coursera-course-analysis\courses_full_dataset.csv"
df_raw = pd.read_csv(data_path) 
df_encoded = encode_coursera_data(df_raw)

# Kiểm tra nhanh xem enroll đã biến thành SỐ chưa
print(df_encoded[['enroll', 'reviews', 'rating']].info())

df_encoded.to_csv('coursera_encoded.csv', index=False)
print("✅ Hoàn tất! Số lượng cột hiện tại:", len(df_encoded.columns))