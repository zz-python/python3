"""挂机脚本

F11 = 开启  F12 = 停止（F11 可再次开启）

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
        self._token = 0

    def _is_running(self, token):
        with self._lock:
            return self._running and self._token == token

    def _loop(self, token):
        kb = keyboard.Controller()
        ms = mouse.Controller()

        round_no = 0
        while self._is_running(token):
            # 仅当当前活跃窗口标题包含“伊莫”时才执行循环
            if picture.WINDOW_TITLE not in picture.active_window_title():
                time.sleep(INTERVAL)
                continue
            round_no += 1
            if round_no > 30000:
                print("[已停止] 达到 300 轮")
                break
            print(f"[第{round_no}轮]")
            # 1. 按下 Tab
            # kb.press(keyboard.Key.tab)
            # time.sleep(0.1)
            # kb.release(keyboard.Key.tab)
            # print("[按下Tab]")
            # time.sleep(0.5)
            # 按下鼠标左键
            # ms.click(mouse.Button.left)
            # print("按下鼠标左键")
            # time.sleep(0.4)
            # 按下F键
            if round_no % 40 == 0:
                kb.press('e')
                kb.release('e')
                print("[按下e]")
                time.sleep(0.2)
                kb.press('r')
                kb.release('r')
                print("[按下r]")
                time.sleep(0.2)
            if round_no % 50 == 0:
                ms.click(mouse.Button.left)
                print("按下鼠标左键")
                time.sleep(0.2)
            kb.press('f')
            kb.release('f')
            print("[按下f]")
            time.sleep(0.2)

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
            self._token += 1
            token = self._token

        self._thread = threading.Thread(target=self._loop, args=(token,), daemon=True)
        self._thread.start()
        print(f"[已开启] 循环：Tab → 截图 → 识别百分比>{PERCENT_THRESHOLD}% 按左键")

    def stop(self):
        with self._lock:
            was_running = self._running
            self._running = False
            self._token += 1
        if was_running:
            print("[已停止]")


def auto():
    presser = AutoPresser()

    def on_press(key):
        if key == keyboard.Key.f11:
            presser.start()
        elif key == keyboard.Key.f12:
            presser.stop()
        elif key == keyboard.Key.f10:
            exit()

    print("挂机脚本已就绪：")
    print("  F11 = 开启")
    print("  F12 = 停止")
    print("  F11 可再次开启")
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        presser.stop()
        print("[已退出]")


if __name__ == "__main__":
    auto()
