import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QWidget, QDesktopWidget, QLabel
from Data import Data


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 导入数据
        l1, l2, LPL_list, LCK_list = Data()

        # 创建主窗口部件
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # 创建布局
        layout = QVBoxLayout(main_widget)

        # 创建字体对象并设置字体属性
        font = QFont()
        font.setFamily("Segue UI")
        font.setPointSize(10)

        # 创建标签控件1（居中对齐的字符串）
        # label1 = QLabel("LPL and LCK Matches")
        label1 = QLabel("S13 Matches")
        label1.setAlignment(Qt.AlignCenter)  # 设置标签的对齐方式为居中对齐
        # 应用字体到标签控件
        label1.setFont(font)
        layout.addWidget(label1)

        # LCK赛程，现在改为S13赛程
        # 创建标签控件2（左对齐的字符串）
        # label2 = QLabel("LPL Today:")
        label2 = QLabel("S13 Today:")
        label2.setAlignment(Qt.AlignLeft)  # 设置标签的对齐方式为左对齐
        # 应用字体到标签控件
        label2.setFont(font)
        layout.addWidget(label2)

        # 创建表格控件1
        table_widget1 = QTableWidget(self)
        table_widget1.setColumnCount(3)  # 设置表格列数
        # 设置表头
        table_widget1.setHorizontalHeaderLabels(['比赛队伍', '比分', '比赛时间'])
        # 隐藏行号
        table_widget1.verticalHeader().setVisible(False)
        # 不允许编辑单元格
        table_widget1.setEditTriggers(QTableWidget.NoEditTriggers)
        # 添加表格项
        table_widget1.setRowCount(l1)  # 设置表格行数
        for i in range(l1):
            for j in range(3):
                item = QTableWidgetItem(LPL_list[j + 3 * i])
                item.setTextAlignment(Qt.AlignCenter)
                table_widget1.setItem(i, j, item)
        # 设置单元格尺寸
        for row in range(l1):
            table_widget1.setRowHeight(row, 40)  # 设置行高为40
        for col in range(3):
            if col != 2:
                table_widget1.setColumnWidth(col, 110)  # 设置列宽为110
            if col == 2:
                table_widget1.setColumnWidth(col, 176)  # 设置列宽为176
        # 将表格控件添加到布局
        layout.addWidget(table_widget1)

        # # LCK赛程
        # # 创建标签控件3（左对齐的字符串）
        # # label3 = QLabel("LCK Today:")
        # label3 = QLabel("S13 Today:")
        # label3.setAlignment(Qt.AlignLeft)  # 设置标签的对齐方式为左对齐
        # # 应用字体到标签控件
        # label3.setFont(font)
        # layout.addWidget(label3)
        #
        # # 创建表格控件2
        # table_widget2 = QTableWidget(self)
        # table_widget2.setColumnCount(3)  # 设置表格列数
        # # 设置表头
        # table_widget2.setHorizontalHeaderLabels(['比赛队伍', '比分', '比赛时间'])
        # # 隐藏行号
        # table_widget2.verticalHeader().setVisible(False)
        # # 不允许编辑单元格
        # table_widget2.setEditTriggers(QTableWidget.NoEditTriggers)
        # # 添加表格项
        # table_widget2.setRowCount(l2)  # 设置表格行数
        # for i in range(l2):
        #     for j in range(3):
        #         item = QTableWidgetItem(LCK_list[j + 3 * i])
        #         item.setTextAlignment(Qt.AlignCenter)
        #         table_widget2.setItem(i, j, item)
        #         # 设置单元格尺寸
        # for row in range(l2):
        #     table_widget2.setRowHeight(row, 40)  # 设置行高为30
        # for col in range(3):
        #     if col != 2:
        #         table_widget2.setColumnWidth(col, 100)  # 设置列宽为100
        #     if col == 2:
        #         table_widget2.setColumnWidth(col, 176)  # 设置列宽为176
        # # 将表格控件添加到布局
        # layout.addWidget(table_widget2)

        # 设置窗口的基本属性
        # 获取屏幕的大小
        screen_info = QDesktopWidget().screenGeometry()
        screen_width = screen_info.width()
        screen_height = screen_info.height()
        # 设置窗口的尺寸和位置
        window_width = 420
        # window_height = 400
        window_height = 300
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.setFixedSize(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        # self.setWindowTitle('LPL&LCK Matches')
        self.setWindowTitle('S13 Matches')

        # 禁用窗口的最大化功能
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
