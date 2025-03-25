import csv

# 你的 CSV 檔案名稱
csv_filename = "dict_idioms_2020_20250102.csv"

# 新的標題
new_header = [
    "id_number", "idiom", "zhuyin", "pinyin", "definition", "source_text_title", 
    "source_text_content", "source_text_annotation", "source_text_reference", 
    "historical_background", "usage_semantic_explanation", "usage_category", 
    "usage_example_sentence", "literary_evidence", "identification_synonyms", 
    "identification_differences", "identification_example_sentence", 
    "form_pronunciation_errors", "synonymous_idioms", "antonymous_idioms", 
    "related_words", "main_entry_non_main_entry"
]

# 讀取原始 CSV，替換標題
with open(csv_filename, "r", encoding="utf-8") as file:
    reader = list(csv.reader(file))
    reader[0] = new_header  # 替換第一行標題

# 寫回 CSV 檔案
with open(csv_filename, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(reader)

print("CSV 標題已成功更新！")
