import pandas as pd

# ====== file input ======
input_file = "coursera_courses_dataset_12.csv"

# ====== file output ======
output_file = "courses_with_category_12.csv"

# ====== category bạn muốn gán ======
category_value = "Physical Science and Engineering"   # sửa ở đây

# ====== đọc dữ liệu ======
df = pd.read_csv(input_file)

# ====== thêm cột category ======
df["category"] = category_value

# ====== ghi ra file mới ======
df.to_csv(output_file, index=False, encoding="utf-8")

print("Đã tạo file mới:", output_file)