import tkinter as tk
from tkinter import messagebox
import random
from game import IdiomGame
from records_database import GameRecord

class IdiomGameGUI:
    def __init__(self, root,):
        self.root = root 
        self.root.title("成語接龍遊戲")
        self.root.geometry("800x600")

        self.game = IdiomGame()
        self.game_record = GameRecord()
        self.player_name = ""
        self.remaining_time = 30
        self.timer_after_id  = None

        # 介面設計
        self.label_welcome = tk.Label(root,
                                      text="歡迎進入成語接龍遊戲", 
                                      font=("PingFang TC", 20, "bold"))
        self.label_welcome.pack()

        self.label_rules = tk.Label(root,
                                    text="""
                                        🎮 遊戲規則如下：
                                        1️⃣ 由電腦先出題，答對者可獲得 5 分
                                        2️⃣ 若當局遊戲持有 3 分以上分數，可用 3 分換取 1 次求救
                                        3️⃣ 每局回答時間限制為 30 秒
                                        4️⃣ 若遊戲途中想離開，請輸入「結束」
                                        歡迎進入成語接龍遊戲
                                        """, 
                                    font=("PingFang TC", 12),
                                    justify="left")
        self.label_rules.pack()

        self.label_timer = tk.Label(root,
                                    text="倒數計時: 30 秒",
                                    font=("PingFang TC", 16),
                                    anchor="s",
                                    fg="red")
        self.label_timer.pack()

        self.label_prompt = tk.Label(root,
                                     text="挑戰者請輸入名字",
                                     font=("PingFang TC", 12),)
        self.label_prompt.pack()

        self.entry_name = tk.Entry(root)
        self.entry_name.pack()

        self.btn_start = tk.Button(root,
                                   text="開始遊戲",
                                   command=self.start_game)
        self.btn_start.pack()

        self.label_current_idiom = tk.Label(root,
                                            text="",
                                            font=("PingFang", 20))
        self.label_current_idiom.pack()

        self.entry_idiom = tk.Entry(root)
        self.entry_idiom.pack()

        self.btn_submit = tk.Button(root,
                                    text="提交",
                                    command=self.check_answer,
                                    state=tk.DISABLED)
        self.btn_submit.pack()

        self.text_log = tk.Text(root, height=10, width=50)
        self.text_log.pack()

    def start_game(self):
        self.player_name = self.entry_name.get().strip()
        if not self.player_name:
            messagebox.showwarning("警告", "請輸入玩家名稱！")
            return
        
        self.text_log.insert(tk.END, f"玩家 {self.player_name} 開始遊戲!\n")
        self.btn_start.config(state=tk.DISABLED)
        self.btn_submit.config(state=tk.NORMAL)

        self.remaining_time = 30
        self.update_timer()

        self.game.current_idiom = random.choice(self.game.idioms_list)
        self.label_current_idiom.config(text=f"💻 電腦先攻：{self.game.current_idiom}")
    
    def update_timer(self):
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
        def countdown():
            if self.remaining_time > 0:
                self.label_timer.config(text=f"倒數計時：{self.remaining_time} 秒")
                self.remaining_time -= 1
                self.timer_after_id = self.root.after(1000, countdown)
            else:
                self.end_game()
        countdown()

    def check_answer(self):
        user_input = self.entry_idiom.get().strip()
        self.entry_idiom.delete(0, tk.END)

        if user_input == "結束":
            self.end_game()
            return
        
        if user_input in self.game.idioms_list and user_input[0] == self.game.current_idiom[-1]:
            self.game.score += 5
            self.text_log.insert(tk.END, f"✅ 正確！目前得分：{self.game.score}\n")
        
            valid_responses = [idiom for idiom in self.game.idioms_list if idiom[0] == user_input[-1]]
            if valid_responses:
                self.game.current_idiom = random.choice(valid_responses)
                self.label_current_idiom.config(text=f"💻 電腦接招：{self.game.current_idiom}")
                self.remaining_time = 30
                self.update_timer()
            else:
                self.text_log.insert(tk.END, "🎉 你贏了！電腦無法接龍！\n")
                self.end_game()
        else:
            self.text_log.insert(tk.END, "❌ 錯誤！請再試一次。\n")
    
    def end_game(self):
        self.text_log.insert(tk.END, f"遊戲結束！{self.player_name} 總得分：{self.game.score}\n")
        self.game_record.save_score(self.player_name, self.game.score)
        self.btn_submit.config(state=tk.DISABLED)
        messagebox.showinfo("遊戲結束", f"{self.player_name} 本次得分：{self.game.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game_gui = IdiomGameGUI(root)
    root.mainloop()