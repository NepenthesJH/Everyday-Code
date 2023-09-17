import numpy as np
from PIL import Image

def image_to_matrix(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    return image_array


def matrix_to_image(matrix, output_path):
    image = Image.fromarray(matrix)
    image.save(output_path)

if __name__ == "__main__":
    image_path = "直角照片.jpg"  # 替换成实际的图像文件路径
    image_matrix = image_to_matrix(image_path)
    height, weight, channels = image_matrix.shape  # 图片尺寸
    n = 60  # 圆角化的半径
    for i in range(height):
        for j in range(weight):
            # 左上角
            if (n - i)**2 + (n - j)**2 > n**2 and i < n and j < n:
                image_matrix[i][j] = [255, 255, 255]
            # 左下角
            if (n - height + i)**2 + (n - j)**2 > n**2 and i > height - n and j < n:
                image_matrix[i][j] = [255, 255, 255]
            # 右上角
            if (n - i)**2 + (n - weight + j)**2 > n**2 and i < n and j > weight - n:
                image_matrix[i][j] = [255, 255, 255]
            # 右下角
            if (n - height + i)**2 + (n - weight + j)**2 > n**2 and i > height - n and j > weight - n:
                image_matrix[i][j] = [255, 255, 255]

    output_path = '圆角照片.jpg'
    matrix_to_image(image_matrix, output_path)
    print("照片圆角化成功！！！")
