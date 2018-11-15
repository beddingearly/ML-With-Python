#coding=utf-8
import math
import operator

class decisiton_tree(object):
    def __init__(self):
        self.createDataSet()
        self.Ent = self.calcShannonEnt(self.dataSet)
        self.bestFeature = 0


    def createDataSet(self):

        self.dataSet = \
                   [[0, 0, 0, 0, 'no'],
                   [0, 0, 0, 1, 'no'],
                   [0, 1, 0, 1, 'yes'],
                   [0, 1, 1, 0, 'yes'],
                   [0, 0, 0, 0, 'no'],
                   [1, 0, 0, 0, 'no'],
                   [1, 0, 0, 1, 'no'],
                   [1, 1, 1, 1, 'yes'],
                   [1, 0, 1, 2, 'yes'],
                   [1, 0, 1, 2, 'yes'],
                   [2, 0, 1, 2, 'yes'],
                   [2, 0, 1, 1, 'yes'],
                   [2, 1, 0, 1, 'yes'],
                   [2, 1, 0, 2, 'yes'],
                   [2, 0, 0, 0, 'no']]
        # 分类属性
        self.labels = ['age', 'work', 'horse', 'credit']

    @staticmethod
    def calcShannonEnt(dataSet):
        '''
        计算总体香浓熵，通过yes/no划分
        -p1 * log2(p1) - p2 * log2(p2)
        :return:
        '''
        numEntries = len(dataSet)
        labelCounts = {}

        # 找到标签中几个yes 几个no
        for i in dataSet:
            currentLabel = i[-1]
            if currentLabel not in labelCounts.keys():
                labelCounts[currentLabel] = 1
            else:
                labelCounts[currentLabel] += 1
        # self.labelCounts = {1: 13, 0: 5}
        shannonEnt = 0.0

        # 计算
        for k in labelCounts.keys():
            prob = float(labelCounts[k]) / numEntries
            shannonEnt -= prob * (math.log(prob, 2))
        return shannonEnt

    @staticmethod
    def splitDataSet(dataSet, axis, value):
        '''
        :param dataSet: 带划分的数据集
        :param axis: 划分数据集的特征
        :param value: 特征的返回值
        :return:去掉一个特征的数据集
        '''
        retDataSet = []
        for featVec in dataSet:
            if featVec[axis] == value:
                reducedFeatVec = featVec[:axis]
                reducedFeatVec.extend(featVec[axis + 1:])
                retDataSet.append(reducedFeatVec)
        '''
        [[0, 0, 0, 'no'], [0, 0, 1, 'no'], [1, 0, 1, 'yes'], [1, 1, 0, 'yes'], [0, 0, 0, 'no']]
        [[0, 0, 0, 'no'], [0, 0, 1, 'no'], [1, 1, 1, 'yes'], [0, 1, 2, 'yes'], [0, 1, 2, 'yes']]
        [[0, 1, 2, 'yes'], [0, 1, 1, 'yes'], [1, 0, 1, 'yes'], [1, 0, 2, 'yes'], [0, 0, 0, 'no']]
        '''
        return retDataSet  # 返回一个列表

    def chooseBestFeatureToSplit(self, dataSet):
        '''
        计算分支结点的信息熵，选择最优的feature
        :return:
        '''
        # [0,0,1,0]
        numFeature = len(dataSet[0]) - 1

        featureList = [[]] * numFeature
        featureEntList = [[0.0]] * numFeature

        for i in range(numFeature):  # 4
            # [0 ,1, 2 ,2, 1, 0, 1]同一行
            featureList[i] = [example[i] for example in dataSet]
            # [0, 1, 2]
            uniqueVals = set(featureList[i])
            tmp = 0
            for value in uniqueVals:
                subDataSet = self.splitDataSet(dataSet, i, value)
                # 数据集特征为i的所占的比例
                prob = len(subDataSet) / float(len(dataSet))
                tmp += prob * self.calcShannonEnt(subDataSet)
            featureEntList[i] = self.Ent - tmp
        bestFeature = featureEntList.index(max(featureEntList))

        return bestFeature, featureEntList

    # 树节点取值的方法，分类树：选取出现最多次数的值，回归树：取所有值的平均值
    # 输入dataList中的一行，输出统计值最大的0/1/2
    # ('classCount', {0: 2, 1: 2, 'yes': 1})
    # ('classCount', {0: 3, 1: 1, 'no': 1})
    def majorityCount(self, classList):
        classCount = {}
        for i in classList:
            if i not in classCount.keys():
                classCount[i] = 0
            classCount[i] += 1

        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)  # 排序，True升序

        # print(sortedClassCount)
        return sortedClassCount[0][0]

    def createTree(self, dataSet, labels):

        # dataSet的最后一列 yes or no
        classList = [example[-1] for example in dataSet]

        # if classList.count(classList[0]) == len(classList):
        #     return classList[0]
        if len(dataSet[0]) == 1:  # 出口
            return self.majorityCount(classList)

        bestFeatureIndex, featureEnt = self.chooseBestFeatureToSplit(dataSet)
        bestFeatureLabel = labels[bestFeatureIndex]
        print('bestFeatureLabel', bestFeatureLabel)

        myTree = {bestFeatureLabel: {}}
        del(labels[bestFeatureIndex])

        featValues = [example[bestFeatureIndex] for example in dataSet]
        uniqueVals = set(featValues)
        for value in uniqueVals:
            subLabels = labels[:]  # 深复制，是通过对象的地址引用进行的赋值
            # 递归调用创建决策树函数
            myTree[bestFeatureLabel][value] = self.createTree(
                self.splitDataSet(dataSet, bestFeatureIndex, value), subLabels)
        return myTree

    def calDynamicEnt(self):
        dataSet1 = self.splitDataSet(self.dataSet, 2, 0)
        dataSet2 = self.splitDataSet(self.dataSet, 2, 1)
        d = dataSet1 + dataSet2
        print d
        leftThreeEnt = self.calcShannonEnt(d)
        print self.Ent
        print leftThreeEnt




if __name__ == '__main__':
    d = decisiton_tree()
    print d.createTree(d.dataSet, d.labels)
    b, f = d.chooseBestFeatureToSplit(d.dataSet)
    # [0.08300749985576883, 0.32365019815155627, 0.4199730940219749, 0.36298956253708536]
    print f
    print b
    d.calDynamicEnt()
    # print d.majorityCount(d.dataSet[1])
    '''
    {'horse':
             {0: {'work':
                      {0: {'age':
                               {0: {'credit': {0: 'no', 1: 'no'}}, 
                                1: {'credit': {0: 'no', 1: 'no'}}, 
                                2: {'credit': {0: 'no'}}}}, 
                       1: {'age': {0: {'credit': {1: 'yes'}}, 
                       2: {'credit': {1: 'yes', 2: 'yes'}}}}}}, 
              1: {'age': {0: {'work': {1: {'credit': {0: 'yes'}}}}, 
                          1: {'work': {0: {'credit': {2: 'yes'}}, 
                                       1: {'credit': {1: 'yes'}}}}, 
                          2: {'work': {0: {'credit': {1: 'yes', 2: 'yes'}}}}}}}}
    '''

