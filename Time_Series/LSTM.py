import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam

np.set_printoptions(precision=4, suppress=True)

# 读取CSV文件到DataFrame
df = pd.read_csv('./Data4.csv')

# 手动归一化
MaxDistance = max(df['Distance'])
MinDistance = min(df['Distance'])
MaxAngle = max(df['Angle'])
MinAngle = min(df['Angle'])
# 归一化前两列
df['TrueDistance'] = (df['TrueDistance'] - MinDistance) / (MaxDistance - MinDistance)
df['TrueAngle'] = (df['TrueAngle'] - MinAngle) / (MaxAngle - MinAngle)
# 归一化后两列，不算真正的归一化
df['Distance'] = (df['Distance'] - MinDistance) / (MaxDistance - MinDistance)
df['Angle'] = (df['Angle'] - MinAngle) / (MaxAngle - MinAngle)

# DataFrame转化为Numpy
df = df.to_numpy()

# 构建时间序列数据
time_steps = 10  # 设置时间步长，可以根据实际情况调整
X = []
y = []

for i in range(len(df) - time_steps):
    X.append(df[i:i+time_steps, 2:])  # 观测值在第2到第3列，根据实际情况调整
    y.append(df[i+time_steps, :2])  # 真实值在第0到第1列，根据实际情况调整

X, y = np.array(X), np.array(y)

# 分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建LSTM模型
model = Sequential()
model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(time_steps, X.shape[2])))
model.add(LSTM(50, activation='relu', return_sequences=True))
model.add(LSTM(50, activation='relu', return_sequences=True))
model.add(LSTM(50, activation='relu'))
model.add(Dense(2))  # 输出两个节点，对应真实值的两列
model.compile(optimizer='adam', loss='mse')

# 设置Adam优化器，并指定学习率
adam_optimizer = Adam(learning_rate=0.01)  # 设置学习率，可以根据需要调整

model.compile(optimizer=adam_optimizer, loss='mse')

# 添加ModelCheckpoint回调函数
checkpoint = ModelCheckpoint("./best_model.h5", save_best_only=True)

# 训练模型，并使用回调函数保存最佳模型
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), callbacks=[checkpoint])

# 在测试集上评估最佳模型
best_model = Sequential()  # 创建一个新模型
best_model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(time_steps, X.shape[2])))
best_model.add(LSTM(50, activation='relu', return_sequences=True))
best_model.add(LSTM(50, activation='relu', return_sequences=True))
best_model.add(LSTM(50, activation='relu'))
best_model.add(Dense(2))
best_model.compile(optimizer=adam_optimizer, loss='mse')

# 加载最佳模型权重
best_model.load_weights("best_model.h5")

# 在整个数据集上进行预测
y_predict = best_model.predict(X)

# 反归一化
predict_data = np.zeros_like(y_predict)
predict_data[:, 0] = y_predict[:, 0] * (MaxDistance - MinDistance) + MinDistance
predict_data[:, 1] = y_predict[:, 1] * (MaxAngle - MinAngle) + MinAngle

# 保存数组到CSV文件
np.savetxt('./predict_data.csv', predict_data, delimiter=',', fmt='%.4f')