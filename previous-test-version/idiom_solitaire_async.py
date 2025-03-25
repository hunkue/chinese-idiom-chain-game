import asyncio
import aioconsole
import pymysql
import random
import time
import os

import pymysql.cursors
from dotenv import load_dotenv

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

print("🔫 準備接招")
print("3")
print("2")
print("1")
print(f"💻 電腦先攻：{current_idiom}")

# 在程式最前面聲明 game_over
global game_over
game_over = asyncio.Event()

async def countdown():
    """倒數計時，每秒更新"""
    start_time = time.time() # 紀錄遊戲開始時間
    for i in range(round_time, 0, -1):
        if game_over.is_set():
            return  # 若遊戲結束則停止計時
        elapsed_time = time.time()-start_time
        print(f"\r倒數計時：{round(round_time - elapsed_time)} 秒", end="", flush=True) # 顯示剩餘時間
        await asyncio.sleep(1)
    game_over.set()  # 時間到，結束遊戲

async def game_round():
    global score, current_idiom, game_over

    try:
        countdown_task = asyncio.create_task(countdown())

        while not game_over.is_set():
            print("\n👉 請輸入你的接龍成語：", end="", flush=True)  # 先顯示提示
            user_input = await asyncio.wait_for(aioconsole.ainput(), timeout=round_time)

            if user_input == "結束":
                print("👋 離開遊戲")
                game_over.set()
                break

            if user_input in idioms_list and user_input[0] == current_idiom[-1]:
                score += 5
                print(f"✅ 正確！目前累積分數：{score}")

                valid_responses = [idiom.strip() for idiom in idioms_list if idiom[0] == user_input[-1]]
                if valid_responses:
                    current_idiom = random.choice(valid_responses)
                    print(f"💻 電腦接招：{current_idiom}")

                    game_over.clear()  # 清除遊戲結束標誌
                    countdown_task = asyncio.create_task(countdown())  # 重新啟動倒數計時
                else:
                    print("🎉 恭喜你贏了！你的對手找不到可以接的成語！")
                    current_idiom = user_input
                    game_over.set()
            else:
                print("❌ 錯誤！再想想看 🤔")

            await countdown_task # 確保倒數計時完成

    except asyncio.TimeoutError:
        print("\n⌛ 時間到！遊戲結束！")
        game_over.set()

async def main():
    global score, current_idiom
    """管理遊戲流程"""

    # 每一輪開始時重設 game_over 事件
    global game_over
    game_over = asyncio.Event()

    countdown_task = asyncio.create_task(countdown())  # 重新啟動倒數計時
    await game_round()  # 執行遊戲回合
    await countdown_task  # 確保倒數計時完成

    # 遊戲結束後顯示結果
    print("\n--------------------------------")
    print(f"\n 本次得分：{score}")
    print("\n--------------------------------")
    print(f"\n📚 最後的成語：{current_idiom}")
    print(f"解釋：{idioms_dict[current_idiom]}")

    # 記錄分數
    record_sql = "INSERT INTO game_records (player_name, score) VALUES (%s, %s);"
    cursor.execute(record_sql, (player_name, score))
    conn.commit()
    cursor.close()
    conn.close()

# 執行遊戲
asyncio.run(main())
