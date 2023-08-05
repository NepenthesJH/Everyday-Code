import numpy as np
import pandas as pd


def Random_Index():
    # 读取昨天的单词索引
    yesterday_words = np.array(pd.read_csv('Words_Index.csv', header=None).tail(2))[0]
    # 总共的单词个数、今天要背的单词索引
    tmp = 1
    today_words = []
    words_numbers = 5651
    # 如果今天生成的单词和昨天有重复的，那么再生成一次
    while tmp != 0:
        today_words = np.random.randint(low=0, high=words_numbers, size=20)
        tmp = np.count_nonzero(today_words == yesterday_words)
    return today_words
