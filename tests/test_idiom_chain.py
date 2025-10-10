import sys
import types
import unittest
from unittest.mock import Mock, patch

try:
    import tkinter as tk
except ModuleNotFoundError:  # pragma: no cover - fallback for CI where tkinter is absent
    class _DummyTkModule:
        NORMAL = "normal"
        DISABLED = "disabled"

    tk = _DummyTkModule()

if "aioconsole" not in sys.modules:
    aioconsole_stub = types.ModuleType("aioconsole")

    async def _dummy_ainput(_prompt):
        return ""

    aioconsole_stub.ainput = _dummy_ainput
    sys.modules["aioconsole"] = aioconsole_stub

if "game_timer" not in sys.modules:
    game_timer_stub = types.ModuleType("game_timer")

    class _DummyEvent:
        def __init__(self):
            self._is_set = False

        def is_set(self):
            return self._is_set

        def set(self):
            self._is_set = True

        def clear(self):
            self._is_set = False

    class _DummyTimer:
        def __init__(self, duration):
            self.duration = duration
            self.stop_event = _DummyEvent()

        def start(self):
            self.stop_event.clear()

        def stop(self):
            self.stop_event.set()

        def get_remaining_time(self):
            return self.duration

        async def countdown(self):
            return None

    game_timer_stub.Timer = _DummyTimer
    sys.modules["game_timer"] = game_timer_stub

if "idiom_database" not in sys.modules:
    idiom_database_stub = types.ModuleType("idiom_database")

    def _dummy_load_idioms_from_db():
        return {}

    idiom_database_stub.load_idioms_from_db = _dummy_load_idioms_from_db
    sys.modules["idiom_database"] = idiom_database_stub

if "records_database" not in sys.modules:
    records_database_stub = types.ModuleType("records_database")

    class _DummyGameRecord:
        def save_score(self, _player, _score):
            return None

    records_database_stub.GameRecord = _DummyGameRecord
    sys.modules["records_database"] = records_database_stub

from idiom_chain import IdiomGameGUI


class DummyEntry:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def delete(self, _start, _end):
        self.value = ""


class DummyText:
    def __init__(self):
        self.records = []

    def insert(self, index, text):
        self.records.append((index, text))


class DummyButton:
    def __init__(self, state):
        self.state = state

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]


class DummyLabel:
    def __init__(self):
        self.text = ""

    def config(self, *, text):
        self.text = text


class IdiomGameGUITest(unittest.TestCase):
    def setUp(self):
        self.gui = IdiomGameGUI.__new__(IdiomGameGUI)
        self.gui.root = Mock()
        self.gui.player_name = ""
        self.gui.remaining_time = 0
        self.gui.timer_after_id = None

        self.gui.entry_name = DummyEntry()
        self.gui.entry_idiom = DummyEntry()
        self.gui.text_log = DummyText()
        self.gui.btn_start = DummyButton(state=tk.NORMAL)
        self.gui.btn_submit = DummyButton(state=tk.DISABLED)
        self.gui.btn_restart_same = DummyButton(state=tk.DISABLED)
        self.gui.btn_restart_new = DummyButton(state=tk.DISABLED)
        self.gui.label_current_idiom = DummyLabel()
        self.gui.update_timer = Mock()

        self.gui.game = Mock()
        self.gui.game.idioms_list = ["測試成語", "另一個成語"]
        self.gui.game.score = 0
        self.gui.game.current_idiom = ""

        self.gui.game_record = Mock()

    def test_start_game_requires_player_name(self):
        with patch("idiom_chain.messagebox.showwarning") as mock_warning:
            self.gui.entry_name.value = ""
            self.gui.start_game()

        mock_warning.assert_called_once_with("警告", "請輸入玩家名稱！")
        self.assertEqual(self.gui.btn_submit.state, tk.DISABLED)
        self.assertFalse(self.gui.text_log.records)
        self.assertEqual(self.gui.game.current_idiom, "")

    def test_start_game_initializes_game_state(self):
        self.gui.entry_name.value = "Alice"

        with patch("idiom_chain.random.choice", return_value="測試成語"):
            self.gui.start_game()

        self.assertEqual(self.gui.player_name, "Alice")
        self.assertEqual(self.gui.btn_start.state, tk.DISABLED)
        self.assertEqual(self.gui.btn_submit.state, tk.NORMAL)
        self.assertEqual(self.gui.btn_restart_same.state, tk.NORMAL)
        self.assertEqual(self.gui.btn_restart_new.state, tk.NORMAL)
        self.gui.update_timer.assert_called_once()
        self.assertEqual(self.gui.remaining_time, 30)
        self.assertEqual(self.gui.game.current_idiom, "測試成語")
        self.assertEqual(self.gui.label_current_idiom.text, "💻 電腦先攻：測試成語")
        self.assertIn("玩家 Alice 開始遊戲!", self.gui.text_log.records[0][1])


if __name__ == "__main__":
    unittest.main()
