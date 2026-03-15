import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data_path = r"E:\University\semeter6\coursera-analy\coursera-course-analysis\craw_data_html\courses_full_dataset.csv"
df_raw = pd.read_csv(data_path)

def visualize_raw_data(df):
    sns.set_theme(style="whitegrid")
    num_cols = [c for c in ['enroll', 'rating', 'reviews'] if c in df.columns]
    
    # 1. Bản đồ rỗng (Missing Values)
    plt.figure(figsize=(10, 4))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
    plt.title('Bản đồ Dữ liệu rỗng (Màu vàng là dòng bị thiếu)', fontsize=14)
    plt.show()

    # 2. Histogram phân phối (Distribution)
    if num_cols:
        fig, axes = plt.subplots(1, len(num_cols), figsize=(18, 5))
        for i, col in enumerate(num_cols):
            sns.histplot(df[col].dropna(), kde=True, ax=axes[i], bins=40, color='royalblue')
            axes[i].set_title(f'Phân phối của {col}')
        plt.tight_layout()
        plt.show()

    # 3. Boxplot phát hiện Ngoại lệ (Outliers)
    if num_cols:
        fig, axes = plt.subplots(1, len(num_cols), figsize=(18, 4))
        for i, col in enumerate(num_cols):
            sns.boxplot(x=df[col].dropna(), ax=axes[i], color='lightcoral')
            axes[i].set_title(f'Boxplot của {col} (Điểm chấm là Outlier)')
        plt.tight_layout()
        plt.show()

    # 4. Ma trận tương quan (Correlation)
    if len(num_cols) > 1:
        plt.figure(figsize=(6, 5))
        corr = df[num_cols].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Ma trận Tương quan (Correlation Matrix)')
        plt.show()

    # 5. Phân phối biến phân loại (Categorical)
    cat_cols = [c for c in ['level', 'duration'] if c in df.columns]
    if cat_cols:
        fig, axes = plt.subplots(1, len(cat_cols), figsize=(14, 5))
        for i, col in enumerate(cat_cols):
            sns.countplot(data=df, x=col, ax=axes[i], order=df[col].value_counts().index, palette='Set2')
            axes[i].set_title(f'Số lượng khóa học theo {col}')
            axes[i].tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()

# Cách gọi hàm:
# df_raw = pd.read_csv('coursera_raw.csv')
visualize_raw_data(df_raw)