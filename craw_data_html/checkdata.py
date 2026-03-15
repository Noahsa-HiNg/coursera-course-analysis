import pandas as pd

# đọc dữ liệu
df = pd.read_csv("courses_full_dataset.csv")

print("Tổng số mẫu:", len(df))
print()

# =========================
# 1. % dữ liệu đầy đủ theo từng cột
# =========================

print("Phần trăm dữ liệu đầy đủ theo từng cột:")

for col in df.columns:
    non_null = df[col].notnull().sum()
    percent = (non_null / len(df)) * 100
    print(f"{col:10s}: {percent:.2f}% ({non_null}/{len(df)})")

print()

# =========================
# 2. số dòng đầy đủ tất cả cột
# =========================

complete_rows = df.dropna()

num_complete = len(complete_rows)
percent_complete = num_complete / len(df) * 100

print("Số mẫu đầy đủ tất cả các trường:", num_complete)
print("Phần trăm mẫu đầy đủ:", f"{percent_complete:.2f}%")

print()

# =========================
# 3. số dòng có missing
# =========================

missing_rows = df.isnull().any(axis=1).sum()

print("Số mẫu có ít nhất 1 giá trị thiếu:", missing_rows)
print("Phần trăm mẫu có missing:", f"{missing_rows/len(df)*100:.2f}%")