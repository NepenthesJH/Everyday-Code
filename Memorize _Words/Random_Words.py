import sys
import csv
import json
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime
from Random_Index import Random_Index


def Random_Words():
    # 读取 JSON 文件
    with open('./Words_JSON/4-CET6-顺序.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()

    # 记录开始背单词的时间和今天的时间
    start_day = datetime(2023, 7, 1)
    today = datetime.today()
    N = (today - start_day).days

    # 今天第几次查看
    n = np.array(pd.read_csv('./Words_Index.csv', header=None).tail(2))[1][0]
    # 如果今天是第一次查看，就生成新的单词索引，反之，不用生成新的
    if n == N:
        # 今天要背的单词索引
        today_words = Random_Index()
        # 把今天的单词写在Yesterday_Words_Index文件里
        with open('Words_Index.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(today_words)
            writer.writerow([n + 1])
            file.close()

    # 创建一个 StringIO 对象来捕获 print() 输出的内容
    output_capturer = StringIO()
    # 将 print() 输出重定向到 StringIO 对象
    sys.stdout = output_capturer

    # 单词的具体内容
    words_index = np.array(pd.read_csv('./Words_Index.csv', header=None).tail(2))[0]
    # 初始化变量
    words = []
    translations = []
    for i in words_index:
        i = int(i)
        words.append(data[i]['word'])
        translations.append(data[i]['translations'])
    # 输出文本，保存为列表
    for h in range(len(words)):
        print(words[h], end=' ' * 16 + '\t')
        tra_tmp = translations[h]
        tra_n = len(tra_tmp)
        for k in range(tra_n):
            print(tra_tmp[k]['type'], end=' ')
            print(tra_tmp[k]['translation'], end=' ')
        print()

    # 将 sys.stdout 重置回原始值（即控制台）
    sys.stdout = sys.__stdout__
    # 将捕获的内容转换为列表形式
    output_lines = output_capturer.getvalue().splitlines()
    # 输出列表内容
    return output_lines
