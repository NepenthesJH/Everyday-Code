import datetime
import re

import requests


def Data():
    url1 = 'https://tiyu.baidu.com/match/lpl/tab/%E8%B5%9B%E7%A8%8B'
    url2 = 'https://tiyu.baidu.com/match/lck/tab/%E8%B5%9B%E7%A8%8B'
    headers = {'Cache-Control': 'no-cache'}
    response1 = requests.get(url1, headers)
    response2 = requests.get(url2, headers)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    pattern1 = re.compile('\{"time":"%s"(.*?)\{"time":"%s"' % (str(today), str(tomorrow)))
    pattern2 = re.compile('.*?"startTime":"(.*?)".*?"leftLogo":\{.*?"name":"(.*?)".*?"score":"(.*?)".*?"rightLogo":\{'
                          '.*?"name":"(.*?)".*?"score":"(.*?)".*?')

    LPL_Result = re.findall(pattern1, response1.text)
    LPL = re.findall(pattern2, str(LPL_Result))

    LCK_Result = re.findall(pattern1, response2.text)
    LCK = re.findall(pattern2, str(LCK_Result))

    # # 控制台输出
    # print("LPL:")
    # print("比赛队伍\t\t比分\t\t比赛时间")
    # l1 = len(LPL)
    # for i in range(l1):
    #     tmp = LPL[i]
    #     print("%s vs %s\t%s:%s\t\t%s" % (tmp[1], tmp[3], tmp[2], tmp[4], tmp[0]))
    #
    # print("LCK:")
    # print("比赛队伍\t\t比分\t\t比赛时间")
    # l2 = len(LCK)
    # for i in range(l2):
    #     tmp = LCK[i]
    #     print("%s vs %s\t%s:%s\t\t%s" % (tmp[1], tmp[3], tmp[2], tmp[4], tmp[0]))

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
