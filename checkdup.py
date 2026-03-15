import pandas as pd

# đọc file
df = pd.read_csv("coursera_courses_dataset.csv")

# tìm các dòng trùng toàn bộ cột
duplicates = df[df.duplicated(keep=False)]

print("Tổng số dòng trong dataset:", len(df))
print("Số dòng trùng nhau:", len(duplicates))

print("\nCác dòng trùng nhau:")
print(duplicates)