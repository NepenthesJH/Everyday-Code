import numpy as np

#异常，输入错误后可以重新进行输入
for i in range(5):
    try:
        # 输入阶数和关系网
        N = int(input("Please input your number of the dots:\n"))
        alpha = float(input("Please input your alpha:\n"))
        Web = {}
        print("Please input your Web")
        # 利用字典存储网络
        for m in range(N):
            line = input()
            line = line.replace(' ', '')
            Web[line[0]] = tuple(line[1:])
        break
    except Exception:
        print("-------------------------------------------------")
        print("Your input is wrong,please check and input again!")

# 把所有的网页做一个记录
keys = Web.keys()
# 进行第一次Map
P_dict = {}.fromkeys(keys, [1 / N])


def Reduce(P_dict, alpha=0.85):
    # 设置alpha
    # 进行reduce
    for char in keys:
        # 计算需要分割的概率
        m = len(Web[char])
        if m != 0:
            p_split = P_dict[char][0] / m
            # 把这些概率分到A、B、C、D头上
            for h in range(m):
                # 这句话意思是在Web关系网中查找A、B、C、D，把它们添加在P_dict对应的概率链里面
                tmp = np.array(P_dict[Web[char][h]])
                tmp = np.append(tmp, p_split)
                P_dict[Web[char][h]] = tmp
    # 把分好的概率再进行求和
    sum_P = 0
    for char in keys:
        tmp = 1 / N * (1 - alpha)
        P_dict[char][0] = 0
        P_dict[char] = [sum(P_dict[char]) * alpha + tmp]
        sum_P += P_dict[char][0]
    # 利用sum_P进行归一化
    for char in keys:
        P_dict[char] = P_dict[char] / sum_P


for i in range(100):
    Reduce(P_dict, alpha)

print(P_dict)
