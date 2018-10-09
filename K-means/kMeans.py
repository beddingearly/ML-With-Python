#coding=utf-8
'''
Created on 2015年11月9日
@author: Administrator
'''
import numpy as np


def kMeans(X, k, maxIt):
    '''

    :param X: 数据集
    :param k: 簇数
    :param maxIt: 执行循环次数
    :return:
    '''


    ### dfafdaf
    # 横纵坐标
    numPoints, numDim = X.shape  # 4 2
    dataSet = np.zeros((numPoints, numDim + 1))
    dataSet[:, : -1] = X
    # 从已有的点集中随机产生新的中心点
    tmp = np.random.randint(numPoints, size=k)
    # print('randint', tmp)
    centroids = dataSet[tmp, :]
    # centroids = dataSet[0:2,:]
    # 给k个中心点标签赋值为[1，k+1]
    # 增加一列是保存簇标签
    #print ('cnetroids1', centroids)
    centroids[:, -1] = range(1, k + 1) # 标签列负值1 2
    #print ('cnetroids2', centroids)

    iterations = 0  # 循环次数
    oldCentroids = None  # 用来储存旧的中心点

    while not shouldStop(oldCentroids, centroids, iterations, maxIt):
        print "iterations:\n ", iterations
        print "dataSet: \n", dataSet
        print "centroids:\n ", centroids

        # 用copy的原因是进行复制，不用=是因为=相当于同时指向一个地址，一个改变另外一个也会改变
        oldCentroids = np.copy(centroids)
        iterations += 1

        # 更新每个点集的中心点label
        updataLabels(dataSet, centroids)

        # 得到新的中心点
        centroids = getCentroids(dataSet, k)

    return dataSet


def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True
    return np.array_equal(oldCentroids, centroids)  # 是否具有相同的结构


def updataLabels(dataSet, centroids):
    '''
    更新标签
    :param dataSet: 数据点集
    :param centroids: 中心坐标点
    :return:
    '''
    numPoints, numDim = dataSet.shape
    for i in range(0, numPoints):
        dataSet[i, -1] = getLabelFromCloseestCentroid(dataSet[i, :-1], centroids)


def getLabelFromCloseestCentroid(dataSetRow, centroids):
    '''

    :param dataSetRow:某个点的二维坐标点
    :param centroids:中心坐标
    :return:
    '''
    label = centroids[0, -1]# 先初始化为一个中心点的标签
    # np.linalg.norm() 计算两个向量之间的距离
    print('dataSetRow', dataSetRow)
    print('cetroids', centroids[0, :-1])
    minDist = np.linalg.norm(dataSetRow - centroids[0, :-1])
    for i in range(1, centroids.shape[0]):#2
        dist = np.linalg.norm(dataSetRow - centroids[i, :-1])# 和两个中心点的距离
        if dist < minDist:
            minDist = dist
            label = centroids[i, -1]

        print "minDist :\n", minDist
        return label


def getCentroids(dataSet, k):
    '''
    更新中心点
    :param dataSet:
    :param k:
    :return: 下次循环的中心点
    '''
    result = np.zeros((k, dataSet.shape[1]))
    for i in range(1, k + 1):# 1 2
        oneCluster = dataSet[dataSet[:, -1] == i, :-1]  # 最后一列即label相等的点集
        result[i - 1, :-1] = np.mean(oneCluster, axis=0)  # 压缩行，对各列求均值
        result[i - 1, -1] = i
    print('result', result)
    return result


x1 = np.array([1, 1])
x2 = np.array([2, 1])
x3 = np.array([4, 3])
x4 = np.array([5, 4])
testX = np.vstack((x1, x2, x3, x4))
print('dataset', testX)
result = kMeans(testX, 2, 3)
print "final result: \n", result