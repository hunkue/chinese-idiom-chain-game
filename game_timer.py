import time
import asyncio

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.stop_event = asyncio.Event()

    def start(self):
        self.start_time = time.time()
        self.stop_event.clear()
    
    def stop(self):
        self.stop_event.set()

    def get_remaining_time(self):
        if self.start_time is None:
            return self.duration
        elapsed_time = time.time() - self.start_time
        return round(max(0, self.duration - elapsed_time))
    
    async def countdown(self):
        while self.get_remaining_time() > 0:
            print(f"\r⌛ 倒數計時：{self.get_remaining_time()} 秒", end="", flush=True)
            if self.stop_event.is_set():
                return
            await asyncio.sleep(1)
        self.stop_event.set()
        print("\n⌛ 時間到！遊戲結束！")