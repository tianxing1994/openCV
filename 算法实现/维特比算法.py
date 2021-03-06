"""
参考资料:
<<统计学习方法>> 李航

维特比算法
维特比算法实际是用动态规划解隐马尔可夫模型预测问题, 即用动态规划求概率最大路径(最优路径). 这时一条路径对应着一个状态序列.
根据动态规划原理, 最优路径具有这样的特性: 如果最优路径在时刻 t 通过结点 i_{t}, 那么这一路径从结点 i_{t} 到络点 i_{T} 的
部分路径, 对于从 i_{t} 到 t_{T} 的所有可能的部分路径来说, 必须是最优的. 因为假如不是这样, 那么从 i_{t} 到 i_{T} 就有另
一条更好的部分路径存在, 如果把它和从 i_{1} 到达 i_{t} 的部分路径连接起来, 就会形成一条原来的路径更优的路径, 这是矛盾的.
依据这一原理, 我们只需要从时刻 t=1 开始, 递推地计算在时刻 t 状态为 i 的各条部分路径的最大概率, 直至得到时刻 t=T 状态为 i
的各条路径的最大概率. 时刻 t=T 的最大概率即为最优路径的概率 P, 最优路径的终结点 i_{T} 也同时得到. 之后, 为了找出最优路径
的各个结点, 从终结点 i_{T} 形始, 由后向前逐步求得结点 i_{t}, ...i_{1}, 得到最优路径 I = (i_{1}, i_{2}, ..., i_{T}).
这就是维特比算法.

首先导入两个变 δ 和 ψ. 定义在时刻 t 状态为 i 的所有单个路径 (i_{1}, i_{2}, ..., i_{t}) 中概率最大值为:
    δ_{t}(i) = max P(i_{t} = i, t_{t-1}, ..., i_{1}, o_{t}, ..., o_{1} | λ), i = 1, 2, ..., N

由定义可得变量 δ 的递推公式:
    δ_{t+1}(i) = max P(i_{t+1} = i, t_{t}, ..., i_{1}, o_{t+1}, ..., o_{1} | λ)
               = max [δ_{t}(j)*a_{ji}] * b_{i}(o_{t+1}), i=1,2,...,N; t=1,2,...,T-1

    其中:
    o_{t}: 表求第 t 次的观测状态.
    a_{ji}: 前一次的隐状态为 j 时, 这一次的隐状态为 i 的概率转换矩阵.
    b_{i}(o_{t}): 由隐状态 i 发射得到观测状态 o_{t} 的概率.
    δ_{t}(j): t 时刻隐状态为 j 的概率.
    δ_{t}(j)*a_{ji}: t 时刻隐状态为 j 的概率乘以隐状态由 j 转换为 i 的概率
    max [δ_{t}(j)*a_{ji}]: t 时刻隐状态为 j, t+1 时刻隐状态为 i 的最大概率.

定义在时刻 t 状态为 i 的所有单个路径 (i_{1}, i_{2}, ..., i_{t-1}, i) 中概率最大的路径的第 t-1 个结点为:
    ψ_{t}(i) = argmax[δ_{t-1}(j)*a_{ji}], i=1,2,...,N

    其中:
    δ_{t}(j): t 时刻隐状态为 j 的概率.
    a_{ji}: 前一次的隐状态为 j 时, 这一次的隐状态为 i 的概率转换矩阵.
    δ_{t-1}(j)*a_{ji}: t-1 时刻的求各隐状态 j 且在 t 时刻隐状态为 i 的概率.
    argmax[δ_{t-1}(j)*a_{ji}]: 求, 指定 t 时刻隐状态为 i 时, t-1 时刻隐状态的最可能值.


维特比算法:
输入: 模型 λ=(A, B, π) 和观测 O=(o_{1}, o_{2}, ..., o_{T});
输出: 最优路径 I=(i_{1}, i_{2}, ..., i_{T}).
(1) 初始化
    δ_{1}(i) = π_{i}b_{i}(o_{1}),   i=1,2,...,N
    ψ_{1}(i) = 0,   i=1,2,...,N

    其中:
    π_{i}: 路径的第 1 个结点, 各隐状态出现的概率.
    o_{t}: t 时刻, 观测状态值.
    b_{i}(o_{1}): 隐状态 i 发射得出观测状态 o_{1} 的概率.
    δ_{1}(i): 1 时刻, 各隐状态的概率.


(2) 递推. 对 t=2,3,...,T
    δ_{t}(i) = max [δ_{t-1}(j)*a_{ji}] * b_{i}(o_{t}),  i=1,2, ...,N
    ψ_{t}(i) = argmax [δ_{t-1}(j)*a_{ji}],  i=1,2, ...,N

    其中:
    δ_{t}(i): t 时刻, 隐状态为 i 的概率.
    a_{ji}: 前一次的隐状态为 j 时, 这一次的隐状态为 i 的概率转换矩阵.
    δ_{t-1}(j)*a_{ji}: t-1 时刻的隐状态为 j , 则 t 时刻的隐状态为 i 的概率.
    max [δ_{t-1}(j)*a_{ji}]: 求 t-1 时刻的隐状态为 j , 则 t 时刻的隐状态为 i 的概率的最大值.
    argmax [δ_{t-1}(j)*a_{ji}]: 求 t-1 时刻的隐状态为 j , 则 t 时刻的隐状态为 i 的概率的最大值对应的 j.
    o_{t}: t 时刻, 观测状态值.
    b_{i}(o_{t}): 隐状态 i 发射得出观测状态 o_{t} 的概率.
    δ_{t}(i): t 时刻的隐状态为 i 的所有可能路径中概率最大的为 max [δ_{t-1}(j)*a_{ji}] * b_{i}(o_{t})
    ψ_{t}(i): t 时刻的隐状态为 i, 则 t-1 时刻的隐状态应为 argmax [δ_{t-1}(j)*a_{ji}]


(3) 终止
    P = max δ_{T}(i)
    i_{T} = argmax [δ_{T}(i)]

    其中:
    P: 在最终时刻 T, 隐状态为 i 的所有可能路径中, 概率最大的路径.
    i_{T}: 在最终时刻 T, 最有可能的隐状态.


(4) 最优路径回溯. 对 t=T-1, T-2, ..., 1
    i_{t} = ψ_{t+1}(i_{t+1})

    其中:
    ψ_{t+1}(i_{t+1}): argmax [δ_{t}(j)*a_{ji}]
    i_{t}: t 时刻的隐状态 i_{t} 等于 t+1 时刻的隐状态为 i_{t+1} 时, t 时刻最有可能的隐状态.

求得最优路径 I=(i_{1}, i_{2}, ..., i_{T}).
"""
import numpy as np


def demo():
    A = np.array([[0.5, 0.2, 0.3],
                  [0.3, 0.5, 0.2],
                  [0.2, 0.3, 0.5]])

    # 每个隐状态观测为 0 的概率和为 1 的概率.
    B = np.array([[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.3]])

    pi = np.array([0.2, 0.4, 0.4]).T

    O = np.array([0, 1, 0])

    # 1. 求 t=1 时刻, 每个隐状态 i 观测得到 O[1] 的概率. sigma_1=[0.1  0.16 0.28]
    sigma_1 = pi * B[:, O[0]]

    # 2. 在 t=2 时刻, 对每个隐状态 i,
    # 求在 t=1 时刻隐状态为 j 观测得到 O[1] 并在 t=2 时刻隐状态为 i 观测得到 O[2] 的路径的最大概率.
    # δ_{t}(i) = max [δ_{t-1}(j)*a_{ji}] * b_{i}(o_{t})
    # sigma_2=[0.028  0.0504 0.042 ]
    proba_2 = (A * np.expand_dims(sigma_1, axis=1)) * B[:, O[1]]
    sigma_2 = np.max(proba_2, axis=0)
    psai_2 = np.argmax(proba_2, axis=0)

    # 3. 在 t=3 时刻
    proba_3 = (A * np.expand_dims(sigma_2, axis=1)) * B[:, O[2]]
    sigma_3 = np.max(proba_3, axis=0)
    psai_3 = np.argmax(proba_3, axis=0)

    # 4. 最优路径的终点隐状态为 2.
    i_T = np.argmax(sigma_3)
    print(i_T)

    # 5. 由最优路径的终点 i_T, 逆向找到 i_2, i_1
    i_2 = np.argmax((A * np.expand_dims(sigma_2, axis=1))[:, i_T])
    print(i_2)

    i_1 = np.argmax((A * np.expand_dims(sigma_1, axis=1))[:, i_2])
    print(i_1)

    # 求得最优路径, I=(2, 2, 2)
    return


def viterbi(A, B, pi, O):
    """将 demo 封装成函数"""
    n = len(O)
    sigma_1 = pi * B[:, O[0]]
    sigma_list = list()
    sigma_list.append(sigma_1)

    # 计算 sigma
    for i in range(1, n):
        sigma = np.max(A * np.expand_dims(sigma_list[-1], axis=1) * B[:, O[i]], axis=0)
        sigma_list.append(sigma)

    # 最优路径的终点隐状态 i_T.
    i_T = np.argmax(sigma_list[-1])

    # 由最优路径的终点 i_T, 逆向求 I.
    I = list()
    I.append(i_T)
    for i in range(n-2, -1, -1):
        sigma = sigma_list[i]
        I_t = np.argmax((A * np.expand_dims(sigma, axis=1))[:, I[-1]])
        I.append(I_t)
    result = list(reversed(I))
    return result


def viterbi_log(pi, A, B, O):
    """
    维特比算法. (对数).
    概率都是小于 1 的数, 多次相乘后, 值变得很小, 会溢出.
    本方法. 对初始向量, 转换概率矩阵, 发射矩阵的概率取对数后计算 (取对数后相乘变为相加).
    """
    pi = np.log(pi + 1e-20)
    A = np.log(A + 1e-20)
    B = np.log(B + 1e-20)

    n = len(O)
    sigma_1 = pi + B[:, O[0]]
    sigma_list = list()
    sigma_list.append(sigma_1)

    # 计算 sigma
    for i in range(1, n):
        sigma = np.max(A + np.expand_dims(sigma_list[-1], axis=1) + B[:, O[i]], axis=0)
        sigma_list.append(sigma)

    # 最优路径的终点隐状态 i_T.
    i_T = np.argmax(sigma_list[-1])

    # 由最优路径的终点 i_T, 逆向求 I.
    I = list()
    I.append(i_T)
    for i in range(n-2, -1, -1):
        sigma = sigma_list[i]
        I_t = np.argmax((A + np.expand_dims(sigma, axis=1))[:, I[-1]])
        I.append(I_t)
    result = np.array(list(reversed(I)))
    return result


def viterbi_demo():
    A = np.array([[0.5, 0.2, 0.3],
                  [0.3, 0.5, 0.2],
                  [0.2, 0.3, 0.5]])

    # 每个隐状态观测为 0 的概率和为 1 的概率.
    B = np.array([[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.3]])

    pi = np.array([0.3, 0.3, 0.4]).T

    O = np.array([0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1])

    result = viterbi(A, B, pi, O)
    print(result)
    return


if __name__ == '__main__':
    viterbi_demo()



























