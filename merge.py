import pandas as pd

# danh sách các file từ 1 đến 12
files = [f"courses_with_category_{i}.csv" for i in range(1, 13)]

dfs = []

for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# nối tất cả dataframe
merged_df = pd.concat(dfs, ignore_index=True)

# ghi ra file mới
merged_df.to_csv("courses_full_dataset.csv", index=False, encoding="utf-8")

print("Đã gộp xong thành file: courses_full_dataset.csv")