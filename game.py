import random
import asyncio
import aioconsole
from game_timer import Timer
from idiom_database import load_idioms_from_db

class IdiomGame:
    def __init__(self, round_time=30):
        self.score = 0
        self.round_time = round_time
        self.timer = Timer(self.round_time)
        self.countdown_task = None
        self.idioms_dict = load_idioms_from_db()
        self.idioms_list = [str(idiom).strip() for idiom in self.idioms_dict.keys()]
        self.current_idiom = ""
    
    def io_input(self, prompt):
        """ 獨立處理 I/O 輸入，未來可替換為 GUI 元件"""
        return aioconsole.ainput(prompt)
    
    def io_print(self, message):
        """ 獨立處理 I/O 輸入，未來可替換為 GUI 元件"""
        print(message)

    async def game_round(self):
        self.timer.start()

        if self.countdown_task is None or self.countdown_task.done():
            self.countdown_task = asyncio.create_task(self.timer.countdown())

        while not self.timer.stop_event.is_set():
            try:
                remaining_time = self.timer.get_remaining_time()
                if remaining_time <= 0:
                    raise asyncio.TimeoutError  # 防止下方 ainput 輸入阻塞
                
                user_input = await asyncio.wait_for(self.io_input("\r👉 請輸入你的接龍成語："), timeout = remaining_time)

                if user_input == "結束":
                    self.io_print("👋 離開遊戲")
                    self.timer.stop()
                    return False 
                
                if user_input in self.idioms_list and user_input[0] == self.current_idiom[-1]:
                    self.score += 5
                    self.io_print(f"✅ 正確！目前累積分數：{self.score}")
                    valid_responses = [idiom.strip() for idiom in self.idioms_list if idiom[0] == user_input[-1]]
                    if valid_responses:
                        self.current_idiom = random.choice(valid_responses)
                        self.io_print(f"💻 電腦接招：{self.current_idiom}")
                        return self.current_idiom, self.score, True
                    else:
                        self.io_print("🎉 恭喜你贏了！你的對手找不到可以接的成語！")
                        self.current_idiom = user_input
                        return user_input, self.score, False
                else:
                    self.io_print("❌ 錯誤！再想想看 🤔")

            except asyncio.TimeoutError:
                self.timer.stop()
                return self.current_idiom, self.score, False