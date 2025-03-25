import pymysql
import random
import time
import threading
import os

import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = db_password,
    database = "game_db",
    charset = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor
)

cursor = conn.cursor()

cursor.execute("SELECT idiom, definition FROM idioms")
idioms_data = cursor.fetchall()
idioms_dict = {row["idiom"]: row["definition"] for row in idioms_data}
idioms_list = [str(idiom).strip() for idiom in idioms_dict.keys()]

print("歡迎進入成語接龍遊戲")
print("""
    🎮 遊戲規則如下：
    1️⃣ 由電腦先出題，答對者可獲得 5 分
    2️⃣ 若當局遊戲持有 3 分以上分數，可用 3 分換取 1 次求救
    3️⃣ 每局回答時間限制為 30 秒
    4️⃣ 若遊戲途中想離開，請輸入「結束」
""")
player_name = input("挑戰者請輸入名字：")

score = 0
round_time = 10
current_idiom = random.choice(idioms_list)
game_over = False
time_up = threading.Event()  # 使用 threading.Event 來協調遊戲結束

print("🔫 準備接招")
#time.sleep(1)
print("3")
#time.sleep(1)
print("2")
#time.sleep(1)
print("1")
#time.sleep(1)
print(f"💻 電腦先攻：{current_idiom}")

def countdown():
    """倒數計時，每秒更新"""
    global game_over
    for i in range(round_time, 0, -1):
        if game_over:
            return  # 如果遊戲結束則停止計時
        print(f"\r⌛ 倒數計時：{i} 秒", end="", flush=True)
        time.sleep(1)

    # 時間到，結束遊戲
    time_up.set()
    print("\n⌛ 時間到！遊戲結束！")

def game_round():
    global score, game_over, current_idiom

    # 啟動計時器
    time_up.clear()
    timer_thread = threading.Thread(target=countdown, daemon=True)
    timer_thread.start()

    while not game_over:
        if time_up.is_set():
            break
        
        user_input = input("\n👉 請輸入你的接龍成語：").strip()

        if user_input == "結束":
            print("👋 離開遊戲")
            game_over = True
            time_up.set()  # 確保倒數計時器停止
            break

        if user_input in idioms_list and user_input[0] == current_idiom[-1]:
            score += 5
            print(f"✅ 正確！目前累積分數：{score}")

            valid_responses = [idiom.strip() for idiom in idioms_list if idiom[0] == user_input[-1]]

            if valid_responses:
                current_idiom = random.choice(valid_responses)
                print(f"💻 電腦接招：{current_idiom}")
                break  # 結束這一輪，進入下一輪
            else:
                print("🎉 恭喜你贏了！你的對手找不到可以接的成語！")
                game_over = True 
                time_up.set()
                break
        else:
            print("❌ 錯誤！再想想看 🤔")
            continue  # 讓玩家繼續嘗試

    timer_thread.join()  # 確保計時器線程結束

# 進行遊戲的輪次
while not game_over:
    game_round()

    if time_up.is_set() or game_over:
        break

print("\n--------------------------------")
print(f"\n 本次得分：{score}")
print("\n--------------------------------")
print(f"\n📚 最後的成語：{current_idiom}")
print(f"解釋：{idioms_dict[current_idiom]}")

record_sql="INSERT INTO game_records (player_name, score) VALUES (%s, %s);"
cursor.execute(record_sql, (player_name, score))
conn.commit()
cursor.close()
conn.close()