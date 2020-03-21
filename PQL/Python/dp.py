import sys
import numpy as np


def laplacian_noise(z,e):
    return np.random.laplace(0, z/e)


def query_with_dp(num, z, e):
    noise = laplacian_noise(z,e)
    return num+noise


if __name__ == "__main__":
    try:
        num = float(sys.argv[1])
        z = float(sys.argv[2])
        e = float(sys.argv[3])
        print(query_with_dp(num,z,e))
    except:
        print('参数错误')
    
