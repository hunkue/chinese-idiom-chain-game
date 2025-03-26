import asyncio
import aioconsole
import pymysql
import random
import time
import os
from dotenv import load_dotenv

import pymysql.cursors

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = pymysql.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="game_db",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
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
round_time = 30
current_idiom = random.choice(idioms_list)
stop_countdown = asyncio.Event()  # 用來控制倒數計時
countdown_task = None
start_time = None

print("🔫 準備接招")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print(f"💻 電腦先攻：{current_idiom}")

def get_remaining_time():
    """計算並返回剩餘時間"""
    elapsed = time.time() - start_time
    return round(max(0, round_time - elapsed))

async def countdown():
    """倒數計時，每秒更新"""
    while get_remaining_time() > 0:
        print(f"\r⌛ 倒數計時：{get_remaining_time()} 秒", end="", flush=True)
        if stop_countdown.is_set():
            return
        await asyncio.sleep(1)

    stop_countdown.set()  # 計時結束，通知遊戲終止
    print("\n⌛ 時間到！遊戲結束！")

async def game_round():
    global score, current_idiom, stop_countdown, countdown_task, start_time

    stop_countdown.clear()
    start_time = time.time()

    # 確保計時器只啟動一次
    if countdown_task is None or countdown_task.done():
        countdown_task = asyncio.create_task(countdown())

    while not stop_countdown.is_set():
        try:
            remaining_time = get_remaining_time()
            if remaining_time <= 0:
                raise asyncio.TimeoutError
            
            print("\r👉 請輸入你的接龍成語：", end="", flush=True)
            user_input = await asyncio.wait_for(aioconsole.ainput(), timeout=remaining_time)

            if user_input == "結束":
                print("👋 離開遊戲")
                stop_countdown.set()
                return False

            if user_input in idioms_list and user_input[0] == current_idiom[-1]:
                score += 5
                print(f"✅ 正確！目前累積分數：{score}")

                valid_responses = [idiom.strip() for idiom in idioms_list if idiom[0] == user_input[-1]]
                if valid_responses:
                    current_idiom = random.choice(valid_responses)
                    print(f"💻 電腦接招：{current_idiom}")
                    return True
                else:
                    print("🎉 恭喜你贏了！你的對手找不到可以接的成語！")
                    current_idiom = user_input
                    return False
            else:
                print("❌ 錯誤！再想想看 🤔")

        except asyncio.TimeoutError:
            stop_countdown.set()
            return False
        
async def main():
    global score, current_idiom

    while True:
        game_continue = await game_round()
        if not game_continue:
            break

    print("\n--------------------------------")
    print(f"\n 本次得分：{score}")
    print("\n--------------------------------")
    print(f"\n📚 最後的成語：{current_idiom}")
    print(f"解釋：{idioms_dict[current_idiom]}")
    print("\n--------------------------------")

    record_sql = "INSERT INTO game_records (player_name, score) VALUES (%s, %s);"
    cursor.execute(record_sql, (player_name, score))
    conn.commit()
    cursor.close()
    conn.close()

asyncio.run(main())
