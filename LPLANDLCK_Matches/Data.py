import datetime
import re

import requests


def Data():
    url1 = 'https://tiyu.baidu.com/match/LPL/tab/%E8%B5%9B%E7%A8%8B'
    url2 = 'https://tiyu.baidu.com/match/LCK/tab/%E8%B5%9B%E7%A8%8B'
    headers = {'Cache-Control': 'no-cache'}
    response1 = requests.get(url1, headers)
    response2 = requests.get(url2, headers)

    today = datetime.date.today()
    month = today.month
    day = today.day
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    pattern1 = re.compile('\{"time":"%s"(.*?)"title":"%s-%s' % (str(today), month, day))
    pattern2 = re.compile('.*?"startTime":"(.*?)".*?"leftLogo":\{.*?"name":"(.*?)".*?"score":"(.*?)".*?"rightLogo":\{'
                          '.*?"name":"(.*?)".*?"score":"(.*?)".*?')

    LPL_Result = re.findall(pattern1, response1.text)
    LPL = re.findall(pattern2, str(LPL_Result))

    LCK_Result = re.findall(pattern1, response2.text)
    LCK = re.findall(pattern2, str(LCK_Result))

    # 矩阵形式输出
    l1 = len(LPL)
    LPL_list = []
    for i in range(l1):
        tmp = LPL[i]
        LPL_list.append(str(tmp[1]) + " vs " + str(tmp[3]))
        LPL_list.append(str(tmp[2]) + ":" + str(tmp[4]))
        LPL_list.append(str(tmp[0]))
    l2 = len(LCK)
    LCK_list = []
    for i in range(l2):
        tmp = LCK[i]
        LCK_list.append(str(tmp[1]) + " vs " + str(tmp[3]))
        LCK_list.append(str(tmp[2]) + ":" + str(tmp[4]))
        LCK_list.append(str(tmp[0]))
    return l1, l2, LPL_list, LCK_list


print("已爬取到数据...")
# l1, l2, LPL_list, LCK_list = Data()
# print(LPL_list)
# print(LCK_list)
