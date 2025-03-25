import pymysql
import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

def load_idioms_from_db():
    db_password = os.getenv("DB_PASSWORD")
    sql = "SELECT idiom, definition FROM idioms;"
    idioms_dict = {}
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password=db_password,
            database="game_db",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                idioms_data = cursor.fetchall()
                idioms_dict = {row["idiom"]: row["definition"] for row in idioms_data}
    except pymysql.MySQLError as e:
        print(f"資料庫錯誤：{e}")

    return idioms_dict