import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

def encode_coursera_data(df):
    df = df.copy()

    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    level_mapping = {
        'Beginner': 1, 
        'Intermediate': 2, 
        'Advanced': 3, 
        'Mixed': 0
    }
    df['level_encoded'] = df['level'].map(level_mapping).fillna(0)
    df = df.drop(columns=['level'])

    duration_mapping = {
        'Less Than 2 Hours': 1, 
        '1-4 Weeks': 2, 
        '1-3 Months': 3, 
        '3-6 Months': 4
    }
    df['duration_encoded'] = df['duration'].map(duration_mapping).fillna(0)
    df = df.drop(columns=['duration'])

    top_20_partners = df['partner'].value_counts().nlargest(20).index
    df['partner_grouped'] = df['partner'].where(df['partner'].isin(top_20_partners), 'Other')
    df = pd.get_dummies(df, columns=['partner_grouped'], prefix='partner', drop_first=False)
    df = df.drop(columns=['partner'])

    if 'category' in df.columns:
        df = pd.get_dummies(df, columns=['category'], prefix='cat', drop_first=False)

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

    tfidf = TfidfVectorizer(max_features=20, stop_words='english')
    title_tfidf = tfidf.fit_transform(df['title'].fillna(''))
    title_encoded = pd.DataFrame(
        title_tfidf.toarray(), 
        columns=[f"title_{w}" for w in tfidf.get_feature_names_out()], 
        index=df.index
    )
    df = pd.concat([df, title_encoded], axis=1)
    df = df.drop(columns=['title'])

    boolean_cols = df.select_dtypes(include='bool').columns
    df[boolean_cols] = df[boolean_cols].astype(int)

    return df

# Cách gọi hàm:
data_path = r"E:\University\semeter6\coursera-analy\coursera-course-analysis\craw_data_html\courses_full_dataset.csv"
df_raw = pd.read_csv(data_path) 
df_encoded = encode_coursera_data(df_raw)
df_encoded.to_csv('coursera_encoded.csv', index=False)