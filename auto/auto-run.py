"""auto-select2.py —— 非活跃（后台）窗口每 1 秒自动按一次 F 键

使用 Win32 API 向指定窗口句柄直接发送 WM_KEYDOWN / WM_KEYUP 消息，
无需窗口处于前台（活跃）状态。

F11 = 开启    F12 = 停止
"""

import ctypes
import threading
import time
from ctypes import wintypes

from pynput import keyboard

# ── 可修改参数 ──────────────────────────────────────────────
WINDOW_TITLE = "zz"   # 目标窗口标题（包含即匹配）
INTERVAL     = 1.0      # 按键间隔（秒）
VK_CODE      = ord("F") # 目标按键字符码（默认 F）

# 常用按键 WM_CHAR 字符码
CHAR_F = ord("F")  # 70
CHAR_R = ord("R")  # 82
CHAR_E = ord("E")  # 69

# ── Win32 ───────────────────────────────────────────────────
user32 = ctypes.windll.user32


# ── 窗口工具（内联，不依赖 picture.py）───────────────────────

def _window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def find_window(title_substr):
    """查找第一个标题包含 title_substr 的可见窗口，返回句柄或 None。"""
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def proc(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        if title_substr in _window_text(hwnd):
            found.append(hwnd)
            return False  # 找到即停止
        return True

    user32.EnumWindows(proc, 0)
    return found[0] if found else None


def active_window_title():
    """返回当前前台（活跃）窗口的标题。"""
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    return _window_text(hwnd)


# ── 按键发送 ────────────────────────────────────────────────

WM_CHAR = 0x0102


def _find_target_control(hwnd):
    """从顶层窗口找到第一个子控件。

    记事本的 Edit 控件才是真正接收 WM_CHAR 的窗口；
    消息发给顶层窗口会被忽略。
    """
    child = user32.GetWindow(hwnd, 5)  # GW_CHILD = 5
    return child if child else hwnd


def send_key(hwnd, vk_code):
    """直接向后台窗口发送 WM_CHAR，无需窗口前台。

    只发 WM_CHAR 不发 WM_KEYDOWN，避免 TranslateMessage
    重复生成字符——每轮只产生一个精确的字符。
    vk_code 即 ASCII 码：大写 'F'=70，小写 'f'=102。
    """
    target = _find_target_control(hwnd)
    user32.PostMessageW(target, WM_CHAR, vk_code, 0)


# ── 鼠标点击（后台）─────────────────────────────────────────

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202
MK_LBUTTON     = 0x0001


def send_mouse_click(hwnd, x=0, y=0):
    """向后台窗口指定坐标发送鼠标左键点击。

    x, y: 相对于窗口客户区的坐标。

    ※ 注意：记事本通过 GetMessagePos() 获取点击坐标，忽略 lParam，
       因此 PostMessage/SendMessage 方式的鼠标点击在记事本中不生效。
       但多数游戏 / 自绘窗口会直接使用 lParam，此时可正常工作。
    """
    target = _find_target_control(hwnd)
    lparam = (y << 16) | (x & 0xFFFF)
    user32.SendMessageW(target, WM_LBUTTONDOWN, MK_LBUTTON, lparam)
    time.sleep(0.05)
    user32.SendMessageW(target, WM_LBUTTONUP, 0, lparam)


# ── 主循环 ──────────────────────────────────────────────────

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
        round_no = 0
        while self._is_running(token):
            round_no += 1

            if round_no > 30000:
                print("[已停止] 达到 30000 轮")
                break

            hwnd = find_window(WINDOW_TITLE)
            if hwnd is None:
                print(f"[{round_no}] 未找到窗口 '{WINDOW_TITLE}'，等待重试…")
                time.sleep(INTERVAL)
                continue

            active_title = active_window_title()
            print(f"[{round_no}] 向窗口 '{WINDOW_TITLE}' 发送 F 键 "
                  f"(当前活跃窗口: '{active_title}')")

            send_mouse_click(hwnd, 100, 100)
            time.sleep(INTERVAL)
            send_key(hwnd, VK_CODE)

            time.sleep(INTERVAL)

    def start(self):
        with self._lock:
            if self._running:
                return
            self._running = True
            self._token += 1
            token = self._token

        self._thread = threading.Thread(target=self._loop, args=(token,), daemon=True)
        self._thread.start()
        print(f"[已开启] 每秒向后台窗口 '{WINDOW_TITLE}' 发送 F 键")

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

    print("后台按键脚本已就绪：")
    print("  F11 = 开启")
    print("  F12 = 停止")
    print("  F10 = 退出")
    print(f"  目标窗口: '{WINDOW_TITLE}'")
    print(f"  间隔: {INTERVAL}s")

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        presser.stop()
        print("[已退出]")


if __name__ == "__main__":
    auto()