import numpy as np
import pandas as pd
import numpy as np
import math
from numpy import array
from pandas import Series, DataFrame

def cal_weight(x):

    x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))


    rows = x.index.size
    cols = x.columns.size
    k = 1.0 / math.log(rows)

    lnf = [[None] * cols for i in range(rows)]


    # p=array(p)
    x = array(x)
    lnf = [[None] * cols for i in range(rows)]
    lnf = array(lnf)
    for i in range(0, rows):
        for j in range(0, cols):
            if x[i][j] == 0:
                lnfij = 0.0
            else:
                p = x[i][j] / x.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(lnf)
    E = lnf


    d = 1 - E.sum(axis=0)

    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj


    w = pd.DataFrame(w)
    print(w)
    return w


def noisyCount(sensitivety, epsilon):
    beta = sensitivety / epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        n_value = -beta * np.log(1. - u2)
    else:
        n_value = beta * np.log(u2)
    print(n_value)
    return n_value


def laplace_mech(data, sensitivety, epsilon):
    for i in range(len(data)):
        data[i] += noisyCount(sensitivety, epsilon)
    return data


if __name__ == '__main__':
    data = [[2, 2, 0, 0, 3, 0], [2, 0, 2, 2, 0, 1], [2, 3, 1, 3, 0, 0], [1, 1, 1, 0, 1, 0], [0, 1, 1, 3, 2, 1], [3, 3, 0, 1, 3, 0], [2, 2, 1, 1, 3, 0], [2, 0, 1, 1, 3, 0], [0, 0, 1, 3, 3, 0], [1, 0, 1, 0, 1, 0], [3, 2, 1, 3, 0, 2], [2, 3, 1, 0, 3, 0]]

    df = DataFrame(data, index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], columns=['1', '2', '3', '4', '5', '6'])
    # print(df)
    df.dropna()
    x = df[0:1]
    print(x)
    w = cal_weight(x)





























# if __name__ == '__main__':
    # df = pd.read_csv('/Users/qiaoyanming/Desktop/工作簿2.csv', encoding='gb2312')
    # # 2数据预处理 ,去除空值的记录
    # df.dropna()
    # print(df)
    # w = cal_weight(df)

    # x = [1., 1., 0.]
    # sensitivety = 1
    # epsilon = 1
    # data = laplace_mech(x, sensitivety, epsilon)
    # print data

    # dic = ['A', 'C', 'G', 'T']
    # l1 = []
    # l2 = []
    #
    # for num in range(0, 12, 1):
    #     a = int(random.randint(0, 3))
    #     b = int(random.randint(0, 3))
    #     c = int(random.randint(0, 3))
    #     d = int(random.randint(0, 3))
    #     e = int(random.randint(0, 3))
    #     f = int(random.randint(0, 3))
    #     str1 = str(dic[a]) + str(dic[b]) + str(dic[c]) + str(dic[d]) + str(dic[e]) + str(dic[f])
    #     # print str1
    #     l1.append(str1)
    #     l3 = [a,b,c,d,e,f]
    #     l2.append(l3)
    #     print l1
    # print l1
    # print l2

    # l1 = ['GGAATA', 'GAGGAC', 'GTCTAA', 'CCCACA', 'ACCTGC', 'TTACTA', 'GGCCTA', 'GACCTA', 'AACTTA', 'CACACA', 'TGCTAG', 'GTCATA']
    # l2 = [[2, 2, 0, 0, 3, 0], [2, 0, 2, 2, 0, 1], [2, 3, 1, 3, 0, 0], [1, 1, 1, 0, 1, 0], [0, 1, 1, 3, 2, 1], [3, 3, 0, 1, 3, 0], [2, 2, 1, 1, 3, 0], [2, 0, 1, 1, 3, 0], [0, 0, 1, 3, 3, 0], [1, 0, 1, 0, 1, 0], [3, 2, 1, 3, 0, 2], [2, 3, 1, 0, 3, 0]]
    # # l1 = ['GGAATT', 'GAGGAC', 'GTCTAA', 'CCCACG', 'ACCTGC', 'TTACTA', 'GGCCTA', 'GATCTC', 'AATTTA', 'CAAACA', 'TGCTAG', 'GTCATA']
    # #
    # # l2 = [[2, 2, 0, 0, 3, 3], [1, 0, 2, 2, 0, 1], [1, 3, 1, 3, 0, 0], [1, 1, 1, 0, 1, 2], [0, 1, 1, 3, 2, 1], [3, 3, 0, 1, 3, 0], [2, 2, 1, 1, 3, 0], [0, 0, 3, 1, 3, 1], [0, 0, 3, 3, 3, 0], [1, 0, 0, 0, 1, 0], [3, 2, 1, 3, 0, 2], [2, 3, 1, 0, 3, 0]]
    # Ac = 0
    # Bc = 0
    # Cc = 0
    # Dc = 0
    #
    # for index in range(len(l2)):
    #     s = l2[index]
    #     s2 = s[5]
    #     if s2 == 0:
    #         Ac = Ac+1
    #     if s2 == 1:
    #         Bc = Bc+1
    #     if s2 == 2:
    #         Cc = Cc+1
    #     if s2 == 3:
    #         Dc = Dc+1
    # print float(Ac)/12
    # print float(Bc)/12
    # print float(Cc)/12
    # print float(Dc)/12

    # import urllib.parse
    # import urllib.request
    #
    # data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding=
    # 'utf8')
    # response = urllib.request.urlopen('http://httpbin.org/post', data = data)
    # print(response.read())







