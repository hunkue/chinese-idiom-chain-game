import pymysql
import pymysql.cursors
import csv
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

# 讀取 csv 檔案的表頭來自動創建資料表
csv_filename = "dict_idioms_2020_20250102.csv"

with open(csv_filename, "r", encoding = "utf-8") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # 取得 csv 表頭欄位名稱（迭代用法）

column_definitions = ", ".join([f"{column} TEXT" for column in header if column.lower() != "id_number"])  # 假設所有欄位都用 TEXT 型別（排除第一個原本csv檔案內的id）
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS idioms (
    id_number INT AUTO_INCREMENT PRIMARY KEY,
    {column_definitions}
);
"""

conn = pymysql.connect(host="localhost",
                       user="root",
                       password=db_password,
                       database="game_db",
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

cursor = conn.cursor()
cursor.execute(create_table_sql)

# cursor.execute("CREATE DATABASE IF NOT EXISTS `game_db`;")
# print("DATABASE 'game_db' is created successfully!")
# cursor.execute("SHOW DATABASES;")
# records = cursor.fetchall() 
# for r in records:
#     print(r)
# cursor.execute("USE `game_db`;")

with open(csv_filename, "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳過表頭到第一列
    
    #動態生成插入語句
    placeholders = ", ".join(["%s"] * len(header))
    insert_sql = f"INSERT INTO idioms ({', '.join(header)}) VALUES ({placeholders});"  # 動態生成佔位符字串
    data = [row for row in csv_reader]  # 取代for row in csv_reader cursor.execute(insert_sql, row)  # 每次插入一行，速度較慢
    cursor.executemany(insert_sql, data)  # 批量插入，提升效能

conn.commit()
cursor.close()
conn.close()

print("CSV is imported in DATABASE 'game_db' successfully!")