# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""
一个带约束的多目标背包问题：
    假设有5类物品，每类物品中包含着四个具体的物品，要求从这五种类别的物品中分别选择一个物品放进背包，
使背包内的物品总价最高，总体积最小，且背包的总质量不能超过92kg。用矩阵P代表背包中物品的价值；
矩阵R代表背包中物品的体积；矩阵C代表物品的质量。P,R,C的取值如下:
P=[[3,4,9,15,2],      R=[[0.2, 0.3, 0.4, 0.6, 0.1],     C=[[10,13,24,32,4],
   [4,6,8,10,2.5],       [0.25,0.35,0.38,0.45,0.15],       [12,15,22,26,5.2],
   [5,7,10,12,3],        [0.3, 0.37,0.5, 0.5, 0.2],        [14,18,25,28,6.8],
   [3,5,10,10,2]]        [0.3, 0.32,0.45,0.6, 0.2]]        [14,14,28,32,6.8]]
分析：
    这是一个0-1背包问题，但如果用一个元素为0或1的矩阵来表示哪些物品被选中，则不利于后面采用进
化算法进行求解。可以从另一种角度对背包问题进行编码：由于问题要求在每类物品均要选出一件，这里我
们可以用0, 1, 2, 3来表示具体选择哪件物品。因此染色体可以编码为一个元素属于{0, 1, 2, 3}的1x5Numpy ndarray一维数组，
比如：[0,0,0,0,0]表示从这五类物品中各选取第一个物品。
"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, M=2):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        maxormins = [-1, 1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 5  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [3] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 添加几个属性来存储P、R、C
        self.P = np.array([[3, 4, 9, 15, 2],
                           [4, 6, 8, 10, 2.5],
                           [5, 7, 10, 12, 3],
                           [3, 5, 10, 10, 2]])
        self.R = np.array([[0.2, 0.3, 0.4, 0.6, 0.1],
                           [0.25, 0.35, 0.38, 0.45, 0.15],
                           [0.3, 0.37, 0.5, 0.5, 0.2],
                           [0.3, 0.32, 0.45, 0.6, 0.2]])
        self.C = np.array([[10, 13, 24, 32, 4],
                           [12, 15, 22, 26, 5.2],
                           [14, 18, 25, 28, 6.8],
                           [14, 14, 28, 32, 6.8]])

    def evalVars(self, Vars):  # 目标函数
        x = Vars.astype(int)
        f1 = np.sum(self.P[x, [0, 1, 2, 3, 4]], 1)
        f2 = np.sum(self.R[x, [0, 1, 2, 3, 4]], 1)
        # 采用可行性法则处理约束
        CV = np.array([np.sum(self.C[x, [0, 1, 2, 3, 4]], 1)]).T - 92
        ObjV = np.vstack([f1, f2]).T
        return ObjV, CV
