"""
Python 连点器 (Auto Clicker)
使用 pyautogui 实现鼠标自动点击。

依赖安装: pip install pyautogui
运行: python autoclicker.py
"""

import time
import threading
import pyautogui

# pyautogui 的安全设置：鼠标移到屏幕左上角可强制停止（防失控）
pyautogui.FAILSAFE = True
# 每次点击之间的最小延迟（秒），设为 0 会非常快
pyautogui.PAUSE = 0.01


class AutoClicker:
    def __init__(self, interval=0.05, clicks=0, button="left"):
        """
        :param interval: 每次点击间隔（秒）
        :param clicks:   点击次数，0 表示无限循环
        :param button:   鼠标按键 left / right / middle
        """
        self.interval = interval
        self.clicks = clicks
        self.button = button
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"[连点器] 已启动，间隔 {self.interval}s，"
              f"{'无限' if self.clicks == 0 else str(self.clicks) + ' 次'}，"
              f"按 Ctrl+C 停止。")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        print("[连点器] 已停止。")

    def _loop(self):
        count = 0
        try:
            while self._running:
                x, y = pyautogui.position()
                pyautogui.click(x=x, y=y, button=self.button)
                count += 1
                if self.clicks and count >= self.clicks:
                    break
                time.sleep(self.interval)
        except pyautogui.FailSafeException:
            print("[连点器] 触发安全停止（鼠标移到左上角）。")
            self._running = False
        finally:
            print(f"[连点器] 共点击 {count} 次。")


def main():
    print("===== Python 连点器 =====")
    interval = float(input("点击间隔（秒，如 0.05）：").strip() or "0.05")
    clicks = int(input("点击次数（0 = 无限）：").strip() or "0")
    button = input("按键（left / right / middle，默认 left）：").strip() or "left"

    clicker = AutoClicker(interval=interval, clicks=clicks, button=button)

    print("将在 3 秒后开始点击，请把鼠标放到目标位置...")
    time.sleep(3)

    clicker.start()
    try:
        while clicker._running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        clicker.stop()


if __name__ == "__main__":
    main()
