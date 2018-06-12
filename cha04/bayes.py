#coding:utf-8
__author__ = 'Yi'
__date__ = '08/06/2018 3:38 PM'

import re

from numpy import *
import feedparser

def loadDataSet():
    postinglist = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]

    classVec = [0, 1, 0 ,1, 0, 1]
    return postinglist, classVec


def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document) # 创建两个集合的并集
    return list(vocabSet)

# 朴素贝叶斯的磁带模型


def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

# 计算条件概率


def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2
    p1Demon = 2
    for i in range(numTrainDocs):
        # 建立矩阵 将整行属性全部都带入
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Demon += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num / p1Demon)
    p0Vect = log(p0Num / p0Denom)
    return  p0Vect, p1Vect, pAbusive

# 朴素的贝叶斯分类器


def classfyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1) # 前面
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

# 测试代码

def testingNB():
    """
    1. 输入数据集及对应的类别
    2. 建立set(储存包含的所有不重复的单词)作为属性值
    3. 建立训练模型：判断每个样本的单词是否存在
    :return:
    """
    listOPosts, listClasses = loadDataSet()
    myVocalList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocalList, postinDoc))
    # 求出对应的概率
    p0V,p1V, pAb = trainNBO(trainMat, listClasses)
    testEntry1 = ['love', 'my', 'dalmation']
    thisDoc1 = array(setOfWords2Vec(myVocalList, testEntry1))
    testEntry2 = ['stupid', 'garbage']
    thisDoc2 = array(setOfWords2Vec(myVocalList, testEntry2))
    print("testentry1 classfied as:", classfyNB(thisDoc1, p0V, p1V, pAb))
    print("testentry2 classfied as:", classfyNB(thisDoc2, p0V, p1V, pAb))

# 处理文本文件


def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w+', bigString)
    return [token.lower() for token in listOfTokens if len(token) > 2]

# 利用贝叶斯进行交叉验证


def spamTest():
    """
    1. docList: 储存所有的样本
    1.1 读取ham 及 spam 当中的文件并经过处理分别以list形式存入
    2. classList: ham中label全为1， spam中label全为0
    3. vocabList: 构建包含所有单词的样本
    4. 随机测试，选取十个测试样本
    5. 将训练样本利用setOfWords2Vec转为向量，构建trainMat
    5. 传入训练样本集利用trainNB计算每个类别P(x/c1) P(x/c2)
    6. 将测试样本逐个带入训练模型，返回的表桥并与标注好的label比较
    :return:
    """
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        # 建立样本集
        docList.append(wordList)
        # 建立词袋
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    # 组合在一起
    vocabList = createVocabList(docList)
    trainingSet = list(range(50))
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        # 将测试样本从样本集中剔除
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNBO(trainMat, array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classfyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print("the error rate is:", float(errorCount)/len(testSet))

# RSS源分类器及高频词汇去除函数


def calcMostFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]


def localWords(feed1, feed0):
    import feedparser
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList) # set
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = list(range(2*minLen))
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(randIndex)
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNBO(trainMat, trainClasses)
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classfyNB(wordVector, p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 0
    print('the error rate is :', float(errorCount)/len(testSet))
    return vocabList, p0V, p1V



if __name__ == "__main__":
    # testingNB()
    # spamTest()
    ny = feedparser.parse("http://newyork.craigslist.org/stp/index.rss")
    print(ny['entries'])
    sf = feedparser.parse("http://sfbay.craigslist.org/stp/index.rss")
    # localWords(ny, sf)
