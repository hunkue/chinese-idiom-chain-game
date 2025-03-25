import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = pymysql.connect(host="localhost",
                       user="root",
                       password=db_password,
                       database="game_db",
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)  # 回傳字典格式資料（原先預設回傳 Tuple）

cursor = conn.cursor()

cursor.execute("SELECT * from idioms LIMIT 1;")
result = cursor.fetchall()
print(result)

cursor.close()
conn.close()