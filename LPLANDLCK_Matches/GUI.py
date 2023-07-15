import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QLabel, QVBoxLayout, QListWidget, QListWidgetItem

from Data import Data

# 导入数据
l1, l2, LPL_list, LCK_list = Data()

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建窗口对象
window = QWidget()

# 设置窗口标题
window.setWindowTitle('LPL&LCK Matches')

# 获取屏幕的大小
screen_info = QDesktopWidget().screenGeometry()
screen_width = screen_info.width()
screen_height = screen_info.height()

# 设置窗口的尺寸和位置
window_width = 440
window_height = 440
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
window.setGeometry(window_x, window_y, window_width, window_height)

# 禁用窗口的最大化功能
window.setWindowFlags(window.windowFlags() & ~Qt.WindowMaximizeButtonHint)

# 创建字体对象并设置字体属性
font = QFont()
font.setFamily("Segue UI")
font.setPointSize(10)

# 创建标签控件1（居中对齐的字符串）
label1 = QLabel("LPL and LCK Matches")
label1.setAlignment(Qt.AlignCenter)  # 设置标签的对齐方式为居中对齐
# 应用字体到标签控件
label1.setFont(font)

# 创建标签控件2（左对齐的字符串）
label2 = QLabel("LPL Today:")
label2.setAlignment(Qt.AlignLeft)  # 设置标签的对齐方式为左对齐
# 应用字体到标签控件
label2.setFont(font)

# 创建列表控件1
list_widget1 = QListWidget()
# 添加项目到列表
item = QListWidgetItem()
item.setText('比赛队伍' + ' ' * 8 + '\t' + '比分' + '\t' + '比赛时间')
list_widget1.addItem(item)

for i in range(l1):
    item = QListWidgetItem()
    item.setText(LPL_list[3 * i + 0] + ' ' * 8 + '\t' + LPL_list[3 * i + 1] + '\t' + LPL_list[3 * i + 2])
    list_widget1.addItem(item)

# 创建标签控件3（左对齐的字符串）
label3 = QLabel("LCK Today:")
label3.setAlignment(Qt.AlignLeft)  # 设置标签的对齐方式为左对齐
# 应用字体到标签控件
label3.setFont(font)

# 创建列表控件2
list_widget2 = QListWidget()
# 添加项目到列表
item = QListWidgetItem()
item.setText('比赛队伍' + ' ' * 8 + '\t' + '比分' + '\t' + '比赛时间')
list_widget2.addItem(item)

for i in range(l2):
    item = QListWidgetItem()
    item.setText(LCK_list[3 * i + 0] + ' ' * 8 + '\t' + LCK_list[3 * i + 1] + '\t' + LCK_list[3 * i + 2])
    list_widget2.addItem(item)

# 创建垂直布局，并将标签添加到布局中
layout = QVBoxLayout()
layout.addWidget(label1)
layout.addWidget(label2)
layout.addWidget(list_widget1)
layout.addWidget(label3)
layout.addWidget(list_widget2)

# 设置窗口的布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序的事件循环
sys.exit(app.exec())
