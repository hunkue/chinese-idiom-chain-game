import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd = db_password,
    database = "game_db",
    charset = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor
)

cursor = conn.cursor()
create_table_sql = """
CREATE TABLE IF NOT EXISTS game_records(
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50),
    score INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
cursor.execute(create_table_sql)

cursor.execute("SHOW TABLES LIKE 'game_records';")
result = cursor.fetchone()

if result:
    print("TABLE 'game_records' exists!")
else:
    print("TABLE 'game_records' does not exist!")

cursor.close()
conn.close()