import numpy as np
import pandas as pd
import os
# 这个代码存在bug，比如说存在同学叫“张大”、“张大大”，以及重名情况

# 读取班级名单
students = pd.read_csv('Students.csv')
students = pd.DataFrame(students)

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
        if homework[j].find(students["姓名"][i]) != -1:
            tmp = 0
            break
    temp_mat[i] = tmp

no_number = np.count_nonzero(temp_mat)

# 这里的have_index、no_index是个元组，调用需要加入下标
have_index = np.where(temp_mat == 0)
no_index = np.where(temp_mat == -1)

print("\n已经交作业的人数:", have_number)
print("已经交作业的人:\n" + students["姓名"][have_index[0]].to_string(index=False))
print("\n未交作业的人数:", no_number)
print("未交作业的人:\n" + students["姓名"][no_index[0]].to_string(index=False))
