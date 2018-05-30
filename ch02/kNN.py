#coding:utf-8
__author__ = 'Yi'
__date__ = '29/05/2018 10:10 PM'


from numpy import *
import operator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.font_manager import _rebuild


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classfy0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    # 沿着X轴复制 dataSetSize倍， Y轴复制一倍：不变
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis=1)
    distance = sqDistance ** 0.5
    sortedDistIndicies = distance.argsort() # 从小到大的索引值
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1 # dict的get方法，如果没有就返回defalut=0
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

"""
goal:使用K-近邻值得算法改进约会网站的配对效果
1. 不喜欢的人
2. 魅力一般的人
3. 极具魅力的人
"""


def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = zeros((numberOfLines, 3))
    index = 0
    classLabelVector = []
    for line in arrayOlines:
        # 去掉空格
        line = line.strip()
        # 用tab分隔整行数据
        listFromLine = line.split("\t")
        returnMat[index, :] = listFromLine[:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


"""
准备数据：归一化特征值
method: newValue = (oldValue-min) / (max-min)
"""

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normalDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normalDataSet = dataSet - tile(minVals, (m, 1))
    normalDataSet = normalDataSet/tile(ranges, (m, 1))
    return normalDataSet, ranges, minVals, m


# 分类器针对约会网站的测试代码

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix("/Users/guapiji/MLInActionCode/Ch02/datingTestSet2.txt")
    normMat, ranges, minVals, m = autoNorm(datingDataMat)
    numTestVecs = int(m*hoRatio)
    errorCount = 0
    for i in range(numTestVecs):
        classfierResult = classfy0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print("the classifier back with: %d, the real answer is : %d" % (classfierResult, datingLabels[i]))
        if (classfierResult != datingLabels[i]):
            errorCount += 1.0
    print("the total error rate is : %f" % (errorCount/numTestVecs))

"""
与会网站预测函数
"""
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent palying video game?"))
    ffMiles = float(input("frequent flier miles earned per years？"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix("/Users/guapiji/MLInActionCode/Ch02/datingTestSet2.txt")
    normMat, ranges, minVals, m = autoNorm(datingDataMat)
    inArr = [percentTats, ffMiles, iceCream]
    classifyResult = classfy0((inArr-minVals)/ranges, normMat, datingLabels, 3)
    print("You will probably like this person: ", resultList[classifyResult-1])


if __name__ == "__main__":
    classifyPerson()
    # _rebuild()
    # group, labels = createDataSet()
    # datingClassTest()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # # size and color
    # ax.scatter(datingDataMat[:,1], datingDataMat[:, 2], 15.0*array(datingLabels), 15.0*array(datingLabels))
    # ax.set_ylabel("每周所消费的冰激凌公升数")
    # ax.set_xlabel("玩视频游戏所消耗的百分比")
    # plt.show()
