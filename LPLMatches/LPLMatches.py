import io
import re
import sys
from collections import OrderedDict
from datetime import date, timedelta

import pandas as pd
import requests
from win10toast import ToastNotifier

# 想看7天的赛程，就n设置为7
n = 1
matches = []
columns = ['比赛队伍', '得分A', '得分B', '比赛日期']
for i in range(n):
    # 获取起始日期
    start = date.today() + timedelta(days=i)
    # 计算终末日期
    end = date.today() + timedelta(days=i + 1)
    url = 'https://apps.game.qq.com/lol/match/apis/searchBMatchInfo_bak.php?p8=5&p1=190&p4=&p2=&p9=' + str(
        start) + '%2000%3A00%3A00&p10=' + str(
        end) + '%2023%3A59%3A59&p6=3&p11=&p12=&page=1&pagesize=9&r1=retObj&_=1687352544442'
    # 发送GET请求到URL，并禁用缓存，以查看表头
    headers = {'Cache-Control': 'no-cache'}
    response = requests.get(url, headers=headers)
    # 这里是非贪婪匹配，才能达到查找所有比赛的需求
    pattern = re.compile(
        '.*?"bMatchName":"(.*?)".*?"ScoreA":"(.*?)".*?"ScoreB":"(.*?)".*?"MatchDate":"(.*?)".*?')
    matches.extend(re.findall(pattern, response.text))

# 去掉重复的并保留前面的元素顺序
matches = list(OrderedDict.fromkeys(matches))
# 转化数据类型
dataframe = pd.DataFrame(matches, columns=columns)
# 获取DataFrame的列名
columns = dataframe.columns.tolist()

# 创建一个新的字符串IO对象
output = io.StringIO()

# 将标准输出重定向到字符串IO对象
sys.stdout = output

# 打印列名
print("%s\t%s\t%s" % (columns[0], '比 分', columns[3]))

# 打印右对齐的数据
for _, row in dataframe.iterrows():
    for col in columns:
        if col == columns[0]:
            print("%s" % row[col], end=' ')
        if col == columns[1]:
            print("\t%s :" % row[col], end=' ')
        if col == columns[2]:
            print("%s" % row[col], end=' ')
        if col == columns[3]:
            print("\t%s" % row[col], end=' ')
    print()

# 恢复标准输出
sys.stdout = sys.__stdout__

# 从字符串IO对象中获取输出结果
output_result = output.getvalue()

# 创建 ToastNotifier 对象
toaster = ToastNotifier()

# 显示通知
toaster.show_toast(title="LPL赛程:", msg=str(output_result), duration=10)
