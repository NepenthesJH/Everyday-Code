import numpy as np
import cv2 as cv
import time

# 取消科学计数法
np.set_printoptions(suppress=True)
# 读取图片
tmp = cv.imread('Test2.png', 0)
# cv.imshow("image", tmp)
# cv.waitKey(5000)
picture = np.array(tmp)
picture_copy = picture.copy()
picture_ysize = picture.shape[0]
picture_xsize = picture.shape[1]

# 直方图向量，0-255
hist = np.zeros(256)
# 滤波器窗口行数、列数，注意这里的xy
window_ysize = 3
window_xsize = 3

# 设置随机种子
img = picture_copy
np.random.seed(42)
# 添加高斯噪声
mean = 0
variance = 200
sigma = variance ** 0.5
gaussian = np.random.normal(mean, sigma, (img.shape[0], img.shape[1]))
noisy_img1 = img + gaussian
# 将像素值限制在[0,255]之间
noisy_img1 = np.clip(noisy_img1, 0, 255)
# 将数据类型转换为无符号8位整数
noisy_img1 = noisy_img1.astype('uint8')
# cv.imshow("nice", noisy_img1)
# cv.waitKey(5000)

# 添加椒盐噪声
# prob 噪声比例
prob = 0.05
thres = 1 - prob
img = picture_copy
noisy_img2 = img.copy()
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        rdn = np.random.rand()
        if rdn < prob:
            noisy_img2[i, j] = 0
        if rdn > thres:
            noisy_img2[i, j] = 255
cv.imshow("Not processed", noisy_img2)
cv.waitKey(5000)

# 本算法忽略边缘处理的问题
th = int(window_xsize * window_ysize / 2)
T1 = time.time()
for i in range(int(window_ysize / 2), int(picture_ysize - window_ysize / 2) + 1):
    # 存储灰度的直方图，对应灰度图
    hist = np.zeros(256)
    # 存储小于中值的灰度数量，对于每一行，这两个值都要初始化
    ltmdn = 0
    # 存储一个窗口中的灰度中值
    mdn = 255
    # 对窗口进行更新
    for j in range(int(window_xsize / 2), int(picture_xsize - window_xsize / 2) + 1):
        if j == int(window_xsize / 2):
            # 建立或者更新每一行的直方图
            for y in range(int(i - window_ysize / 2), int(i + window_ysize / 2) + 1):
                for x in range(int(j - window_xsize / 2), int(j + window_xsize / 2) + 1):
                    hist[picture_copy[y, x]] = hist[picture_copy[y, x]] + 1
            # 求出中值
            for h in range(256):
                ltmdn = ltmdn + hist[h]
                if ltmdn > th:
                    mdn = h
                    ltmdn = ltmdn - hist[h]
                    break

        if j > int(window_xsize / 2):
            # 对直方图进行更新
            # 查找左右两列，并进行更新
            left_index = j - int(window_xsize / 2) - 1
            right_index = j + int(window_xsize / 2)

            step = int(i - window_ysize / 2)
            left_column = picture_copy[step:window_ysize + step, left_index]
            right_column = picture_copy[step:window_ysize + step, right_index]

            for k in range(window_ysize):
                # 对左侧的列进行删减
                gl = left_column[k]
                hist[gl] = hist[gl] - 1
                if gl < mdn:
                    ltmdn = ltmdn - 1
                # 对右侧的列进行添加
                gl = right_column[k]
                hist[gl] = hist[gl] + 1
                if gl < mdn:
                    ltmdn = ltmdn + 1
            # 找出中值
            if ltmdn > th:
                while ltmdn > th:
                    mdn = mdn - 1
                    ltmdn = ltmdn - hist[mdn]
            else:
                while ltmdn + hist[mdn] <= th:
                    ltmdn = ltmdn + hist[mdn]
                    mdn = mdn + 1
        noisy_img2[i, j] = mdn
T2 = time.time()
time = (T2 - T1) * 1000

cv.imshow('Processed', noisy_img2)
cv.waitKey(5000)
# 时间处理
print("这是一个%dx%d的模板，运行时间为%d毫秒" % (window_ysize, window_xsize, time))
