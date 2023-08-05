import sys
import random
from time import time
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QFontMetrics
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel


class HandSpeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置全局字体
        self.font1 = QFont("YouYuan", 24)
        self.font2 = QFont("YouYuan", 22)
        self.font3 = QFont("YouYuan", 18)
        # 创建主窗口部件
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # 设置窗口的基本属性
        # 获取屏幕的大小
        screen_info = QDesktopWidget().screenGeometry()
        screen_width = screen_info.width()
        screen_height = screen_info.height()
        # 设置窗口的尺寸和位置
        window_width = 800
        window_height = 600
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.setFixedSize(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle('反应测试')
        # 禁用窗口的最大化功能
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 创建一个水平布局，并将其设置为主窗口的布局
        layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 生成三个按钮
        # 设置按钮的通用属性
        button_width = 200
        button_height = 80
        button_x = (window_width - button_width) // 2
        button_y = (window_height - button_height) // 2
        # 生成一个开始按钮
        # 设置按钮字体和大小
        self.start_button = QPushButton("开始测试", self)
        self.start_button.setFixedSize(button_width, button_height)
        self.start_button.setGeometry(button_x, button_y, button_width, button_height)
        self.start_button.setFont(self.font1)

        # 生成两个功能性按钮，“再测一次”和“历史数据”
        # *再测一次*
        # 设置按钮字体和大小
        self.again_button = QPushButton("再测一次", self)
        self.again_button.setFixedSize(button_width, button_height)
        self.again_button.setGeometry(button_x - 180, button_y + 120, button_width, button_height)
        self.again_button.setFont(self.font1)
        # *历史数据*
        # 设置按钮字体和大小
        self.data_button = QPushButton("历史数据", self)
        self.data_button.setFixedSize(button_width, button_height)
        self.data_button.setGeometry(button_x + 180, button_y + 120, button_width, button_height)
        self.data_button.setFont(self.font1)
        # 按钮的开始状态
        self.start_button.show()
        self.again_button.hide()
        self.data_button.hide()
        # 连接按钮点击事件到槽函数
        self.start_button.clicked.connect(self.on_button_clicked)
        self.again_button.clicked.connect(self.on_button_clicked)
        self.data_button.clicked.connect(self.data_list)
        # 将按钮放到布局中
        # layout.addWidget(self.start_button)
        # layout.addWidget(self.again_button)
        # layout.addWidget(self.data_button)

        # 初始化标识是否显示文字的属性，分为0、1、2
        # 注:0档代表未点击按钮，1档代表点击按钮之后、绿屏未出现，2档代表绿屏出现之后
        self.show_text = 0
        # 记录点击次数
        self.clicked_number = 0
        # 初始化时间变量
        self.timer = QTimer(self)
        self.start_time = None
        self.end_time = None
        self.testing_time = None
        # 存储数据
        self.user_data = []
        # 记录时间
        self.user_datetime = []

    def on_button_clicked(self):
        # 测试环境初始化
        # 隐藏按钮
        self.start_button.hide()
        self.again_button.hide()
        self.data_button.hide()
        # 触发窗口重新绘制
        self.show_text = 1
        # 绿屏随机出现时间
        random_time = random.randint(a=3000, b=7000)
        # 如果已经测试过一次，那就先把时间器断开
        if self.clicked_number == 1:
            self.timer.timeout.disconnect(self.clear_text)
        # 调整点击次数
        self.clicked_number = 0
        # 设置定时器，在random_time秒后执行clear_text函数
        self.timer.start(random_time)
        if self.clicked_number == 0:
            self.timer.timeout.connect(self.clear_text)
        self.update()

    def paintEvent(self, event):
        # 绘制文字
        if self.show_text == 1 and self.clicked_number == 0:
            painter = QPainter(self)
            painter.setPen(Qt.black)
            painter.setFont(self.font2)
            painter.drawText(self.rect(), Qt.AlignCenter, "请看到绿色时点击屏幕")
        if self.show_text == 2 and self.clicked_number == 1:
            painter = QPainter(self)
            painter.setPen(Qt.black)
            painter.setFont(self.font2)
            metrics = QFontMetrics(self.font2)
            text_width = metrics.width(f"本次测试反应时间为: {round(self.testing_time)} ms")
            text_height = metrics.height()
            x = round((self.width() - text_width) / 2)
            y = round((self.height() - text_height) / 2) - 120
            painter.drawText(x, y, self.width(), self.height(), Qt.AlignLeft,
                             f"本次测试反应时间为: {round(self.testing_time)} ms")
            # 重新设置按钮状态
            self.start_button.hide()
            self.again_button.show()
            self.data_button.show()

    def clear_text(self):
        # 文字消失，窗口背景变为绿色
        self.show_text = 2
        if self.show_text == 2 and self.clicked_number == 0:
            self.start_time = time()
            self.setStyleSheet("background-color: #72FF93;")
        self.update()

    def mousePressEvent(self, event):
        # 当窗口背景为绿色且未点击过窗口时，点击窗口后恢复原来的颜色，并且再次点击无效
        if self.show_text == 2 and self.clicked_number == 0:
            self.setStyleSheet("")
            self.end_time = time()
            self.testing_time = 1000 * (self.end_time - self.start_time)
            self.clicked_number += 1
            # 记录测试时间和反应速度
            self.user_data.append(round(self.testing_time))
            self.user_datetime.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def data_list(self):
        # 历史数据环境初始化
        # 隐藏按钮
        self.start_button.hide()
        self.again_button.hide()
        self.data_button.hide()
        # 创建一个主布局
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 创建文本标签
        # 创建标签控件（居中对齐的字符串）
        label = QLabel("历史数据")
        label.setAlignment(Qt.AlignCenter)  # 设置标签的对齐方式为居中对齐
        label.setFont(self.font3)
        layout.addWidget(label)

        # 创建表格控件
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(3)  # 设置表格列数
        # 设置表头
        table_widget.setHorizontalHeaderLabels(['序号', '反应速度', '测试时间'])
        # 隐藏行号
        table_widget.verticalHeader().setVisible(False)
        # 不允许编辑单元格
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        # 添加表格项
        l = len(self.user_data)
        table_widget.setRowCount(l)  # 设置表格行数
        for i in range(l):
            item1 = QTableWidgetItem(str(i))
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem(str(self.user_data[i]) + ' ms')
            item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem(self.user_datetime[i])
            item3.setTextAlignment(Qt.AlignCenter)
            table_widget.setItem(i, 0, item1)
            table_widget.setItem(i, 1, item2)
            table_widget.setItem(i, 2, item3)
        # 设置单元格尺寸
        for row in range(l):
            table_widget.setRowHeight(row, 40)  # 设置行高
        # 设置列宽
        table_widget.setColumnWidth(0, 258)
        table_widget.setColumnWidth(1, 258)
        table_widget.setColumnWidth(2, 260)

        # # 将表格控件添加到布局
        layout.addWidget(table_widget)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandSpeedWindow()
    window.show()
    sys.exit(app.exec_())
