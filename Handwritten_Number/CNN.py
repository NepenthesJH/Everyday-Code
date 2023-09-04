import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 定义超参数
input_size = 20  # 处理后的图像为20*20
num_classes = 10  # 类别数为10
num_epochs = 10  # 训练的总循环周期为10
batch_size = 64  # 指定批次大小，即64张图片
shuffle = True  # 是否洗牌数据

# 训练集
train_dataset = datasets.MNIST(root='C:/CodeFile/Data', train=True, transform=transforms.ToTensor(), download=True)
# 测试集
test_dataset = datasets.MNIST(root='C:/CodeFile/Data', train=False, transform=transforms.ToTensor(), download=True)
# 构建batch数据
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(  # 输入大小(28, 28, 1)
            nn.Conv2d(
                in_channels=1,  # 灰度图为1层
                out_channels=16,  # 特征图个数
                kernel_size=5,  # 卷积核大小
                stride=1,  # 卷积移动步长
                padding=2  # 边缘填充的像素值，padding = (kernel_size - 1) / 2
            ),
            nn.ReLU(),  # RELU层
            nn.MaxPool2d(kernel_size=2)  # 池化操作(2*2)，输出结果为(14, 14, 16)
        )
        self.conv2 = nn.Sequential(  # 输入大小(14, 14, 16)
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 输出大小(7, 7, 32)
        )
        self.out = nn.Linear(7 * 7 * 32, 10)  # 全连接层的结果

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # Flatten操作，结果为(batch_size, 5 * 5 * 32)
        output = self.out(x)
        return output


# 评估标准
def accuracy(predictions, labels):
    pred = torch.max(predictions.data, 1)[1]
    rights = pred.eq(labels.data.view_as(pred)).sum()
    return rights, len(labels)


# 实例化
cnn = CNN()
# 损失函数
criterion = nn.CrossEntropyLoss()
# 优化器
optimizer = optim.Adam(cnn.parameters(), lr=0.001)  # 随机梯度下降法

# 检查CUDA是否可用
if torch.cuda.is_available():
    print("CUDA 可用")
else:
    print("CUDA 不可用")
# 模型和数据迁移到GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cnn.to(device)

# 开始训练循环
for epoch in range(num_epochs):
    # 当前epoch的结果保存下来
    train_rights = []

    for batch_idx, (data1, target1) in enumerate(train_loader):  # 针对容器中的每一个批次进行操作
        # 迁移数据
        data1 = data1.to(device)
        target1 = target1.to(device)
        # 开始训练
        cnn.train()
        output = cnn(data1)
        loss = criterion(output, target1)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        right = accuracy(output, target1)
        train_rights.append(right)

        if batch_idx % 100 == 0:
            cnn.eval()
            val_rights = []

            for (data2, target2) in test_loader:
                # 迁移数据
                data2 = data2.to(device)
                target2 = target2.to(device)
                # 开始检验
                output = cnn(data2)
                right = accuracy(output, target2)
                val_rights.append(right)


            # 准确率计算
            train_r = (sum([tup[0] for tup in train_rights]), sum([tup[1] for tup in train_rights]))
            val_r = (sum([tup[0] for tup in val_rights]), sum([tup[1] for tup in val_rights]))
            # 输出训练过程
            print('epoch:{} [{}/{} ({:.0f}%)]\tloss:{:.6f}\ttrain accuracy:{:.2f}%\t test accuracy:{:.2f}%'.format(
                epoch, batch_idx * batch_size, len(train_loader.dataset),
                       100 * batch_idx / len(train_loader),
                loss.data,
                       100 * train_r[0] / train_r[1],
                       100 * val_r[0] / val_r[1]
            ))
