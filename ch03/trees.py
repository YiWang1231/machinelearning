#coding:utf-8
__author__ = 'Yi'
__date__ = '31/05/2018 4:10 PM'

import operator

from math import log

from ch03 import treePlotter

def calcShannonEnt(dataSet):
    # 计算样本的数量
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        shannonEnt = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key])/numEntries
            shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

# 划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

# 计算不同划分的shannnoEnt，并计算信息增益


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    # 循环所有的feature计算每一个信息熵增
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList) # 去处重复值
        newEntropy = 0.0
        # 计算分支点的信息熵增
        # 1.将样本根据feature不同的取值分类
        # 2.对每一类求分支点信息增伤
        # 3.infoGain = totalEnt - (dv/d*Ent(dv)) v = 1 to numbers of probablity
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

# 递归构建决策树


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classList[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
# 构建树的函数代码


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    # 如果都属于同一类则返回该值
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    """
    迭代计算
    1. 循环子节点传入新的dataSet
    2. 利用choseBestFeatureTopSplit()计算dataSet最优划分
    3. 建立新的tree节点
    4. 继续迭代，直到分类一致 return classList[0]
    """
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        subDataSet = splitDataSet(dataSet, bestFeat, value)
        myTree[bestFeatLabel][value] = createTree(subDataSet, subLabels)
    return myTree


# 使用决策树分类函数

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


# 决策树的储存

def storeTree(inputTree):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


if __name__ == "__main__":
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lenseLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lenseLabels)
    print(lensesTree)
    treePlotter.createPlot(lensesTree)
    # print(classify(lensesTree, lenseLabels, []))
    # myData, label = createDataSet()
    # # print(label)
    # myTree = createTree(myData, label)
    # print(myTree)
    # print(classify(myTree, ['no surfacing', 'flippers'], [0, 1]))
    # print(chooseBestFeatureToSplit(myData))
    # print(splitDataSet(myData, 0, 1))
