from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTextBrowser, QMessageBox, QFormLayout, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import time
import uuid

class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("基础信息")
        self.resize(1600, 900)  

        # 设置布局
        main_layout = QVBoxLayout()

        # 创建表单布局
        formLayout = QFormLayout()
        formRow1Layout = QHBoxLayout()
        formRow2Layout = QHBoxLayout()
        formRow3Layout = QHBoxLayout()
        formLayout.addRow(formRow1Layout)
        formLayout.addRow(formRow2Layout)
        formLayout.addRow(formRow3Layout)
        main_layout.addLayout(formLayout)

        self.timesLabel = QLabel("测试次数:")
        self.timesEdit = QLineEdit("10")
        formRow1Layout.addWidget(self.timesLabel)
        formRow1Layout.addWidget(self.timesEdit)

        self.url1Label = QLabel("测试url:")
        self.url1Edit = QLineEdit("http://101.35.20.226/demo/query/test?param=${random}")
        formRow2Layout.addWidget(self.url1Label)
        formRow2Layout.addWidget(self.url1Edit)

        self.remarkLabel = QLabel("url中${random}将替换乘随机数")
        formRow3Layout.addWidget(self.remarkLabel)


        self.testDbButton = QPushButton("开始测试", self)
        main_layout.addWidget(self.testDbButton)
        self.textLog = QTextBrowser()
        main_layout.addWidget(self.textLog)
        self.setLayout(main_layout)
        self.testDbButton.clicked.connect(self.testDb)

    def testDb(self):
        # url = "http://101.35.20.226/demo/query/test"
        # self.textLog.append(f"测试请求url={url}")
        # self.testHttpN(url)
        urls = [self.url1Edit.text()]
        times = int(self.timesEdit.text())
        self.worker = Worker(urls, times)
        self.worker.update_signal.connect(self.update_text_browser)
        # 启动线程
        self.worker.start()

    def update_text_browser(self, text, clear_last_line):
        # 在主线程中更新 QTextBrowser
        if clear_last_line:
            self.clear_last_line()
        self.textLog.append(text)

    def clear_last_line(self):
        text = self.textLog.toPlainText()  # 获取全部文本
        print(f"text={text}")
        lines = text.splitlines()              # 分割成行列表
        if lines:                              # 如果有内容
            lines = lines[:-1]                 # 删除最后一行
            self.textLog.setText('\n'.join(lines))  # 重新设置文本


class Worker(QThread):
    # 定义一个信号，用于传递文本到主线程
    update_signal = pyqtSignal(str, bool)

    def __init__(self, urls=None, times=10):
        super().__init__()
        self.urls = urls
        self.times = times
    
    def run(self):
        for url in self.urls:
            self.update_signal.emit(f"{url},开始测试", False)
            elapsed_time_count = []
            for i in range(self.times):
                if "${random}" in url:
                    random_uuid = uuid.uuid4()
                    print(f"random_uuid={random_uuid}")
                    url_format = url.replace("${random}", str(random_uuid))
                else:
                    url_format = url
                elapsed_time = round(self.testHttp(url_format) * 1000)
                self.update_signal.emit(f"{url_format},第{i+1}次测试，用时{elapsed_time}毫秒", False if i==0 else True)
                elapsed_time_count.append(elapsed_time)
            max_value = max(elapsed_time_count)
            min_value = min(elapsed_time_count)
            avg_value = sum(elapsed_time_count) / len(elapsed_time_count)
            self.update_signal.emit(f"{url},测试完成，最大值={max_value}，最小值={min_value}，平均值={avg_value}", False)

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