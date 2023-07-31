import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Random_Words import Random_Words
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QLabel, QDesktopWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # 导入单词
        Data = Random_Words()

        # 创建菜单栏和菜单项
        menubar = self.menuBar()

        # 创建主窗口部件
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # 创建布局和列表
        layout = QVBoxLayout(main_widget)

        # 创建字体对象并设置字体属性
        font = QFont()
        font.setFamily("Segue UI")
        font.setPointSize(12)

        # 创建标签控件（居中对齐的字符串）
        label = QLabel("今天の单词")
        label.setAlignment(Qt.AlignCenter)  # 设置标签的对齐方式为居中对齐
        # 应用字体到标签控件
        label.setFont(font)
        layout.addWidget(label)

        # 创建列表
        list_widget = QListWidget()
        # 向列表中添加一些项目
        list_widget.addItems(Data)

        # 将列表添加到布局
        layout.addWidget(list_widget)

        # 设置窗口的基本属性
        # 获取屏幕的大小
        screen_info = QDesktopWidget().screenGeometry()
        screen_width = screen_info.width()
        screen_height = screen_info.height()
        # 设置窗口的尺寸和位置
        window_width = 800
        window_height = 500
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle('六级单词，背！背！背！')

        # 禁用窗口的最大化功能
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
