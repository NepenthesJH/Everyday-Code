import numpy as np
import pandas as pd
import os

# 读取班级名单
students = pd.read_csv('Students.csv')
students = np.array(students)
# 读取作业文件夹，实际使用把作业文件夹放到这个项目里面，修改文件夹名字即可
file_dir = "./测试作业"
for root, dirs, homework in os.walk(file_dir, topdown=False):
    print("当前目录路径：\n", root)
    print("读取到的文件夹：\n", dirs)
    print("读取到的文件：\n", homework)
# 进行姓名和文件的比较，如果存在就返回0,不存在就返回-1
total_number = len(students)
have_number = len(homework)
temp_mat = np.zeros(total_number)
for i in range(total_number):
    tmp = -1
    for j in range(have_number):
        if homework[j].find(students[i][1]) != -1:
            tmp = 0
            break
    temp_mat[i] = tmp

no_number = np.count_nonzero(temp_mat)

have_index = np.where(temp_mat == 0)
no_index = np.where(temp_mat == -1)

print("已经交作业的人数：", have_number)
print("已经交作业的人：\n", students[have_index].T)
print("未交作业的人数：", no_number)
print("未交作业的人：\n", students[no_index].T)
