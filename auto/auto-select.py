"""挂机脚本

F11 = 开启  F12 = 退出程序

循环流程：
    按 Tab → 截图 + 打印截图日志 → OCR 识别百分比“xx%”
    → 大于 45 才按鼠标左键，否则回到下一轮按 Tab 继续判断。
"""

import threading
import time

from pynput import keyboard, mouse

import picture  # 复用截图与 OCR 判断逻辑

INTERVAL = 0.5  # 每轮间隔 500 毫秒
PERCENT_THRESHOLD = 45  # 识别到百分比大于该值时按下鼠标


class AutoPresser:
    def __init__(self):
        self._running = False
        self._lock = threading.Lock()
        self._thread = None

    def _is_running(self):
        with self._lock:
            return self._running

    def _loop(self):
        kb = keyboard.Controller()
        ms = mouse.Controller()

        round_no = 0
        while self._is_running():
            # 仅当当前活跃窗口标题包含“伊莫”时才执行循环
            if picture.WINDOW_TITLE not in picture.active_window_title():
                time.sleep(INTERVAL)
                continue
            round_no += 1
            if round_no > 300:
                print("[已停止] 达到 300 轮")
                break
            print(f"[第{round_no}轮]")
            # 1. 按下 Tab
            kb.press(keyboard.Key.tab)
            time.sleep(0.1)
            kb.release(keyboard.Key.tab)
            print("[按下Tab]")
            time.sleep(0.5)
            ms.click(mouse.Button.left)
            time.sleep(0.4)
            print("按下鼠标左键")

            # # 2. 截图 + 打印截图日志
            # print("[按下Tab] 正在截图并判断…")
            # detect_start = time.perf_counter()
            # path = picture.screenshot()
            # if path is None:
            #     print("[跳过] 未找到“伊莫”窗口")
            #     time.sleep(INTERVAL)
            #     continue

            # # 3. 识别百分比，大于阈值才按鼠标左键
            # percent = picture.detect_percent(path)
            # detect_time = time.perf_counter() - detect_start
            # if percent > PERCENT_THRESHOLD:
            #     print(f"[命中] {detect_time:.3f}s 识别到 {percent}%")
            #     ms.click(mouse.Button.left)
            #     print(" 按下鼠标左键")
            # else:
            #     print(f"[未命中] {detect_time:.3f}s 识别到 {percent}%")

    def start(self):
        with self._lock:
            if self._running:
                return
            self._running = True

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"[已开启] 循环：Tab → 截图 → 识别百分比>{PERCENT_THRESHOLD}% 按左键")

    def stop(self):
        with self._lock:
            was_running = self._running
            self._running = False
        if was_running:
            print("[已关闭]")


def auto():
    presser = AutoPresser()

    def on_press(key):
        if key == keyboard.Key.f11:
            presser.start()
        elif key == keyboard.Key.f12:
            presser.stop()
            print("[退出程序]")
            return False  # 停止监听器，结束程序

    print("挂机脚本已就绪：")
    print("  F11 = 开启")
    print("  F12 = 退出程序")
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        presser.stop()
        print("[已退出]")


if __name__ == "__main__":
    auto()
