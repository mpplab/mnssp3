#导入工具库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential 
from keras import layers 
from keras import regularizers
from sklearn.model_selection import train_test_split 
from sklearn.metrics import roc_curve, auc


# 加载数据集
data = "data.csv"
df = pd.read_csv(data, header=0, index_col=0)
"""
查看数据集的head和信息
"""
# print(df.head())
# print(df.info())


"""
设置标签：
将目标变量转换为癫痫(y列编码为1)与非癫痫(2-5)

即将癫痫的目标变量设置为1，其他设置为标签0
"""
df["seizure"] = 0 
for i in range(11500): 
    if df["y"][i] == 1: 
        df["seizure"][i] = 1 
    else:
        df["seizure"][i] = 0

# plt.plot(range(178), df.iloc[11496,0:178]) 
# plt.show()


"""
将把数据准备成神经网络可以接受的形式。
首先解析数据，
然后标准化值，
最后创建目标数组
"""
# 创建df1来保存波形数据点(waveform data points) 
df1 = df.drop(["seizure", "y"], axis=1)
# 1. 构建11500 x 178的二维数组
wave = np.zeros((11500, 178))

z=0
for index, row in df1.iterrows():
    wave[z,:] = row
    z +=1

# 打印数组形状
# print(wave.shape) 
# 2. 标准化数据
# """
# 标准化数据，使其平均值为0，标准差为1
# """
# mean = wave.mean(axis=0) 
# wave -= mean 
# std = wave.std(axis=0) 
# wave /= std 
# 3. 创建目标数组
target = df["seizure"].values


"""
创建模型
"""
model = Sequential() 
model.add(layers.Dense(64, activation="relu", kernel_regularizer=regularizers.l1(0.001), input_shape = (178,))) 
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64, activation="relu", kernel_regularizer=regularizers.l1(0.001))) 
model.add(layers.Dropout(0.5)) 
model.add(layers.Dense(1, activation="sigmoid")) 
model.summary()


"""
利用sklearn的train_test_split函数将所有的数据的20%作为测试集，其他的作为训练集
"""
x_train, x_test, y_train, y_test = train_test_split(wave, target, test_size=0.2, random_state=42)

# #编译机器学习模型
model.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["acc"])


"""
训练模型
epoch为100，
batch_size为128，
设置20%的数据集作为验证集
"""
history = model.fit(x_train, y_train, epochs=100, batch_size=128, validation_split=0.2, verbose=2)

model.save('model_save/epilepsy_detection_model_x.h5')

# # 测试数据(预测数据)
# y_pred = model.predict(x_test).ravel()
# # 计算ROC
# fpr_keras, tpr_keras, thresholds_keras = roc_curve(y_test, y_pred) 
# # 计算 AUC
# AUC = auc(fpr_keras, tpr_keras)
# # 绘制 ROC曲线
# plt.plot(fpr_keras, tpr_keras, label='Keras Model(area = {:.3f})'.format(AUC)) 
# plt.xlabel('False positive Rate') 
# plt.ylabel('True positive Rate') 
# plt.title('ROC curve') 
# plt.legend(loc='best') 
# plt.show()


