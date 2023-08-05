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
    image_path = "白底照片.jpg"  # 替换成实际的图像文件路径
    image_matrix = image_to_matrix(image_path)
    for i in np.arange(640):
        for j in np.arange(480):
            if image_matrix[i][j][0] > 180 and image_matrix[i][j][1] > 180 and image_matrix[i][j][2] > 180:
                image_matrix[i][j][0] = 50
                image_matrix[i][j][1] = 150
                image_matrix[i][j][2] = 255

    output_path = '蓝底照片.jpg'
    matrix_to_image(image_matrix, output_path)
    print("照片换底成功！！！")
