import gzip
import os

import cv2
import numpy as np
from scipy import ndimage


# 加载本地mnist数据集
def load_data(data_folder):
    # 60000行的训练数据集（mnist.train）和10000行的测试数据集（mnist.test）
    # 每一个MNIST数据单元有两部分组成：一张包含手写数字的图片和一个对应的标签.
    # 每个数字图片大小是28×28像素，一共分成10类，分别是0到9，共10个数字.
    files = [
        'train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
        't10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz'
    ]

    paths = []
    for fname in files:
        paths.append(os.path.join(data_folder, fname))

    with gzip.open(paths[0], 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[1], 'rb') as imgpath:
        x_train = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)

    with gzip.open(paths[2], 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[3], 'rb') as imgpath:
        x_test = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)

    x_train = processing_data(x_train)
    x_test = processing_data(x_test)

    return (x_train, y_train), (x_test, y_test)


def processing_data(X):
    N = len(X)
    # 连通性检验，由于数字0-9都是“连通”的，没有“连通”的矩阵可以实现预处理
    # 进行数字形态学的膨胀和腐蚀，让这些“数字”尽可能满足连通
    X_matrix = np.zeros_like(X)
    # 对每个训练图像进行处理
    n_train = 0
    for matrix in X:
        # 进行连通性检验
        labeled_matrix, num_features = ndimage.label(matrix)
        # 定义核掩模，进行开操作，去噪
        if num_features > 1:
            labeled_matrix = ndimage.binary_opening(labeled_matrix, structure=np.ones([3, 3]), iterations=1)
        X_matrix[n_train] = labeled_matrix
        n_train = n_train + 1
    # 通过上面对图像的处理，得到的图像将不再是灰度图像，而是二值图像，不需要考虑灰度值，反而更简化了计算

    # 对每个图片的“数字”进行向左上角平移
    # 找一下所有数字的最大长度和高度
    w_max = 0
    h_max = 0
    for i in range(N):
        image = X_matrix[i]
        # 找到图像的边界
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x_min = 100
        y_min = 100
        for contour in contours:
            x_axis, y_axis, weight, height = cv2.boundingRect(contour)
            if x_min > x_axis:
                x_min = x_axis
            if y_min > y_axis:
                y_min = y_axis
            if weight > w_max:
                w_max = weight
            if height > h_max:
                h_max = height
        # 计算平移距离
        shift_x = x_min
        shift_y = y_min
        # 平移图像内容
        rows, cols = image.shape
        M = np.float32([[1, 0, -shift_x], [0, 1, -shift_y]])
        X_matrix[i] = cv2.warpAffine(image, M, (cols, rows))

    # 裁剪数据
    X_400 = X_matrix[:, :20, :20].copy()
    # 再把数字平移到中心
    for i in range(N):
        image = X_400[i]
        # 找到图像的边界
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        w_max = 0
        h_max = 0
        for contour in contours:
            x_axis, y_axis, weight, height = cv2.boundingRect(contour)
            if weight > w_max:
                w_max = weight
            if height > h_max:
                h_max = height
        # 计算平移距离
        shift_x = (20 - w_max) / 2
        shift_y = (20 - h_max) / 2
        # 平移图像内容
        rows, cols = image.shape
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        X_400[i] = cv2.warpAffine(image, M, (cols, rows))
        # 把数据转化成400*1
        # X = X_400.reshape(N, 400)
    return X_400


# 指定正确的数据文件夹路径。这里是测试调用
# (train_images, train_labels), (test_images, test_labels) = load_data('C:/CodeFile/Data/MNIST/raw')
