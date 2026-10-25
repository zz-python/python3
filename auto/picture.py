"""屏幕截图脚本

截取标题包含“伊莫”的窗口中心 300×150（宽×高）区域，保存到脚本所在目录的 tmp 目录。
"""

import ctypes
import os
import re
from ctypes import wintypes

import mss

WINDOW_TITLE = "伊莫"
CENTER_WIDTH = 200   # 中心区域宽（px）
CENTER_HEIGHT = 100  # 中心区域高（px）

user32 = ctypes.windll.user32


def _enable_dpi_awareness():
    # 让 GetWindowRect 返回物理像素，与 mss 坐标一致（高分屏必需）
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def _window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def find_window(title_substr):
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
    """返回当前前台（活跃）窗口的标题，找不到返回空字符串。"""
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    return _window_text(hwnd)


def list_window_titles():
    titles = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def proc(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        text = _window_text(hwnd)
        if text:
            titles.append(text)
        return True

    user32.EnumWindows(proc, 0)
    return titles


def window_rect(hwnd):
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


def center_region(rect, width, height):
    left, top, right, bottom = rect
    cx = (left + right) // 2
    cy = (top + bottom) // 2
    return {
        "left": cx - width // 2,
        "top": cy - height // 2,
        "width": width,
        "height": height,
    }


def screenshot():
    _enable_dpi_awareness()

    hwnd = find_window(WINDOW_TITLE)
    if hwnd is None:
        print(f'[未找到窗口] 标题包含“{WINDOW_TITLE}”的窗口')
        titles = list_window_titles()
        print("当前可见窗口标题：")
        for t in titles:
            print(f"  - {t}")
        return None

    region = center_region(window_rect(hwnd), CENTER_WIDTH, CENTER_HEIGHT)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_dir = os.path.join(base_dir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    filename = "newest.png"  # 固定文件名，每次截图覆盖上一次
    filepath = os.path.join(tmp_dir, filename)

    with mss.MSS() as sct:
        shot = sct.grab(region)
        mss.tools.to_png(shot.rgb, shot.size, output=filepath)

    print(f"[已保存] {filepath}  区域={region}")
    return filepath


_ocr_engine = None


def contains_text(image_path, keyword="背袭"):
    """对图片做 OCR，判断是否包含指定字符。

    返回 True 表示图片中检测到该字符，False 表示未检测到。
    """
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr_engine = RapidOCR()

    result, _ = _ocr_engine(image_path)
    if not result:
        return False
    for item in result:
        text = item[1]
        if keyword in text:
            return True
    return False


def detect_percent(image_path):
    """对图片做 OCR，识别出形如“xx%”的百分比数值。

    识别到则返回该整数（如 50、100），未识别到返回 -1。
    """
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr_engine = RapidOCR()

    result, _ = _ocr_engine(image_path)
    if not result:
        return -1
    for item in result:
        text = item[1]
        match = re.search(r"(\d+)%", text)
        if match:
            return int(match.group(1))
    return -1


if __name__ == "__main__":
    path = screenshot()
    if path:
        hit = contains_text(path, "背袭")
        print(f"[OCR] {'检测到' if hit else '未检测到'}“背袭”")

