# _*- coding = utf-8 -*-
# @Time : 2022/8/1 20:16
# @Author : Administrator张晨
# @File : neural network.py
# @Software : PyCharm
import numpy as np
import scipy.special
import matplotlib.pyplot



# 定义神经网络类
class neuralNetwork:
    # 初始化神经网络 设置3层（输入层 隐藏层 输出层）节点数、学习率
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # 设置每一层的节点数
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # 设置 链接权重矩阵 wih who
        # 权重因子在矩阵中是 从i层到j层链接因子为 wij
        # w11 w21
        # w12 w22
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))

        # 设置学习率
        self.lr = learningrate

        # 设置激活函数为sigmoid
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    # 训练神经网络
    def train(self, inputs_list, targets_list):

        # 转化输入和目标为列
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # 计算输入到隐藏层
        hidden_inputs = np.dot(self.wih, inputs)
        # 计算隐藏层输出
        hidden_outputs = self.activation_function(hidden_inputs)

        # 计算输入到输出层
        final_inputs = np.dot(self.who, hidden_outputs)
        # 计算输出层输出
        final_outputs = self.activation_function(final_inputs)

        # 计算目标和输入经过计算的结果偏差
        outputs_errors = targets - final_outputs
        # 隐藏层的偏差 为输出层偏差 根据权重进行分配
        hidden_errors = np.dot(self.who.T, outputs_errors)

        # 更新隐藏层和输出层之间的权重因子
        self.who += self.lr * np.dot((outputs_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        # 更新输入层和隐藏层之间的权重因子
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

        pass

    # 查询神经网络
    def query(self, inputs_list):
        # 传入输入列表list 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        # 计算输入到隐藏层
        hidden_inputs = np.dot(self.wih, inputs)
        # 计算隐藏层输出
        hidden_outputs = self.activation_function(hidden_inputs)

        # 计算输入到输出层
        final_inputs = np.dot(self.who, hidden_outputs)
        # 计算输出层输出
        final_outputs = self.activation_function(final_inputs)
        return final_outputs


# 设置神经网络的参数
inputnodes = 784
hiddennodes = 100
outputnodes = 10
learningrate = 0.3
# 创建神经网络对象
n = neuralNetwork(inputnodes, hiddennodes, outputnodes, learningrate)

# 训练神经网络的数据输入处理
training_data_file = open("mnist_train_100.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

# 设置神经网络训练的世代次数
epochs = 5
for e in range(epochs):
    for record in training_data_list:
        # 把读入的列表通过","分开  变成一个785的列表
        all_values = record.split(',')
        # 把0~255之间的数字组成的灰度图，转成0.01~1.0之间
        inputs = (np.asfarray(all_values[1:])/255.0*0.99)+0.01
        # 建立对应的目标结果 目标为0.01~0.9  对的标签对应改为0.9
        targets = np.zeros(outputnodes) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass

# 测试神经网络的数据输入处理
test_data_file = open("mnist_train_10.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

# 测试神经网络输出并统计正确率
scorecard = []      #定义一个正确与否的统计列表
# 测试所有的数据
for record in test_data_list:
    all_values = record.split(',')
    correct_label = int(all_values[0])
    inputs = (np.asfarray(all_values[1:])/255.0*0.99)+0.01
    outputs = n.query(inputs)
    label = np.argmax(outputs)
    if label == correct_label:
        scorecard.append(1)
    else:
        scorecard.append(0)
        pass
    pass

scorecard_array = np.asfarray(scorecard)
print("正确率=%.2f"%(scorecard_array.sum()/scorecard_array.size*100))
'''
# 测试其中一次查询 并图形显示
all_values = test_data_list[3].split(',')
print(all_values[0])
print(n.query(np.asfarray(all_values[1:])/255.0*0.99+0.01))
image_array = (np.asfarray(all_values[1:])).reshape(28,28)
matplotlib.pyplot.imshow(image_array,cmap='Greys', interpolation='None')
matplotlib.pyplot.show()
'''

if __name__ == '__main__':
    print("主程序运行完成")
