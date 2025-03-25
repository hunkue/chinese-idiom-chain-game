import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class GameRecord:
    def save_score(self, player_name, score):
        db_password = os.getenv("DB_PASSWORD")
        sql = "INSERT INTO game_records (player_name, score) VALUES (%s, %s);"
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password=db_password,
                database="game_db",
                charset="utf8mb4",
            )
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (player_name, score))
                    conn.commit()
                print(f"玩家 {player_name} 的分數已儲存")
        except Exception as e:
            print(f"無法儲存分數：{e}")