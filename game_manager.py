import time
import random
from game import IdiomGame
from records_database import GameRecord

class GameManager:
    def __init__(self):
        self.game = IdiomGame()
        self.game_record = GameRecord()
        self.player_name = ""

    def show_welcome_message(self):
        print(f"歡迎進入成語接龍遊戲")
        print("""
            🎮 遊戲規則如下：
            1️⃣ 由電腦先出題，答對者可獲得 5 分
            2️⃣ 若當局遊戲持有 3 分以上分數，可用 3 分換取 1 次求救
            3️⃣ 每局回答時間限制為 30 秒
            4️⃣ 若遊戲途中想離開，請輸入「結束」
        """)

    def show_countdown_message(self):
        print("🔫 準備接招")
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)  # 模擬倒數計時
        print("遊戲開始！")

    def show_game_result(self):
        print(f"{self.player_name} 本次得分：{self.game.score}")

    def show_final_idiom(self):
        print(f"📚 最後的成語：{self.game.current_idiom}")
        print(f"解釋：{self.game.idioms_dict[self.game.current_idiom]}")

    def save_score_to_database(self):
        self.game_record.save_score(self.player_name, self.game.score)

    async def start_game(self):
        self.show_welcome_message()
        self.player_name = input("挑戰者請輸入名字：")
        self.show_countdown_message()
        self.first_idiom = random.choice(self.game.idioms_list)
        print(f"💻 電腦先攻：{self.first_idiom}")
        self.game.current_idiom = self.first_idiom
        while True:
            game_continue = await self.game.game_round()
            if not game_continue:
                self.show_game_result()
                self.show_final_idiom()
                self.save_score_to_database()
                break