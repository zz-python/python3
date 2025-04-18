from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTextBrowser, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import time

class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("基础信息")
        self.resize(1600, 900)  

        # 设置布局
        layout = QVBoxLayout()

        self.testDbButton = QPushButton("测试连接", self)
        layout.addWidget(self.testDbButton)
        self.textLog = QTextBrowser()
        layout.addWidget(self.textLog)
        self.setLayout(layout)
        self.testDbButton.clicked.connect(self.testDb)

    def update_text_browser(self, text, clear_last_line):
        # 在主线程中更新 QTextBrowser
        self.textLog.append(text)

    def testDb(self):
        # url = "http://101.35.20.226/demo/query/test"
        # self.textLog.append(f"测试请求url={url}")
        # self.testHttpN(url)

        self.worker = Worker()
        self.worker.update_signal.connect(self.update_text_browser)
        # 启动线程
        self.worker.start()

    def testHttpN(self, url): 
        for i in range(100):
            print(i)
            self.textLog.append(f"第{i}次请求")
            self.testHttp(url)

        

    def testHttp(self, url):
        
        # 目标 URL
        #url = "http://example.com"


        start_time = time.time()
        # 发送 GET 请求
        response = requests.get(url)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"GET 请求用时: {elapsed_time:.4f} 秒")
        print(f"GET 请求用时: {elapsed_time*1000}毫秒")

        # 检查请求是否成功
        if response.status_code == 200:
            # 获取页面内容
            page_content = response.text
            print(page_content)
        else:
            print(f"请求失败，状态码: {response.status_code}")

        return elapsed_time

    def clear_last_line(self):
        # 获取 QTextCursor
        cursor = self.textLog.textCursor()
        # 定位到文本的末尾
        cursor.movePosition(cursor.End)
        # 向上移动一行，定位到最后一行的起始位置
        cursor.movePosition(cursor.Up)
        # 删除这行内容
        cursor.removeSelectedText()

class Worker(QThread):
    # 定义一个信号，用于传递文本到主线程
    update_signal = pyqtSignal(str, bool)
    
    def run(self):
        # 模拟耗时操作，逐步发送文本
        for i in range(1, 11):
            self.update_signal.emit(f"Step {i}/10: Task in progress...\n", True)
            self.msleep(1000)  # 每秒更新一次
        
        self.update_signal.emit("Task Completed!", True)  # 最后显示完成信息