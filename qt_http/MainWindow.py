import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QMainWindow, QPushButton, QMessageBox
from InfoWindow import InfoWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口的标题和大小
        self.setWindowTitle(f'网络测试')
        self.resize(1200, 800)

        # 创建主窗口的中央小部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建顶部的按钮布局
        button_layout = QHBoxLayout()
        # 创建两个按钮
        self.buttonInfo = QPushButton("http测试")
        self.buttonInfo.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.buttonLog = QPushButton("grpc测试")
        self.buttonLog.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.buttonTask = QPushButton("http3测试")
        self.buttonTask.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")

        # 将按钮添加到布局中
        button_layout.addWidget(self.buttonInfo)
        button_layout.addWidget(self.buttonLog)
        button_layout.addWidget(self.buttonTask)

        self.stacked_widget = QStackedWidget()
        self.infoWindow = InfoWindow()
        # self.logWindow = LogWindow()
        # self.taskWindow = TaskWindow()

        self.stacked_widget.addWidget(self.infoWindow)
        # self.stacked_widget.addWidget(self.logWindow)
        # self.stacked_widget.addWidget(self.taskWindow)


        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        self.buttonInfo.clicked.connect(self.showInfoWindow)
        # self.buttonLog.clicked.connect(self.showLogWindow)
        # self.buttonTask.clicked.connect(self.showTaskWindow)
    
    def showInfoWindow(self):
        self.stacked_widget.setCurrentWidget(self.infoWindow)

    def showLogWindow(self):
        self.stacked_widget.setCurrentWidget(self.logWindow)

    def showTaskWindow(self):
        self.stacked_widget.setCurrentWidget(self.taskWindow)
        #self.show_child3_signal.emit()

if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)
    # 创建窗口对象
    window = MainWindow()
    # 显示窗口
    window.show()
    # 进入主事件循环
    sys.exit(app.exec_())