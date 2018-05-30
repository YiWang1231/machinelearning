# Chapter02 Summary
## Step One: Bulid the kNN algorithms
```
# inX:the test data
# dataSet: the training data
# labels: the labels of the training data ,all the labels are correct 
# k: chose the k element of the results which have mimimal distance with the test data
def classfy0(inX, dataSet, labels, k):
    dataSize = dataSet.shape[0] # get the total rows of hte dataSet
    diff = tile(inX, (dataSize, 1)) - dataSet # tile(data, (m, n)) m:copy the data for m times in row, n:copy the data n times in column
    # calculate the distance we need the square of the diffenence of every dimension
    sqDiff = diff ** 2 
    # then we need to sum the square of the difference
    sqDistance = sqDiffMat.sum(axis=1)
    # the ge the distance
    distance = sqrt(sqDistance)
    # then get the index rank of the every distance by ascending
    sortedDistances = distance.argsort()
    classCount = {}
    for i in range(k):
        vertorlabel = labels[sortedDistances[i]]
        # get(vectorLabel, 0) mean if vectorLabel already in dict get the exact number or get 0
        classCount[vectorLabel] = classCount.get(vectorLabel, 0)  +1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        
```

## Step Two: transfer file to vector
```
# from this function we need to get 
def file2matrix(filename):
    fr = open(filename)
    arrOLines = fr.readlines() # seperate file in line
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOflines, 3))
    classLabelVector = []
    index = 0
    for i in range(len(arrayOLines)):
        line = line.strip()
        listFromeLine = line.split('\t')
        returnMat[i, :] = listFromLine[:3]
        classLabelVector.addpend(int(listFromline[-1]))
    return returnMat, classLabelVector
```

## Step Three: normalization the number

```

# use the definiton of the normalization
# newVals= (oldValues - min)/(max - min)
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normalDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normalDataSet = dataSet - tile(minVals, (m, 1))
    normalDataSet = normalDataSet/tile(ranges, (m, 1))
    return normalDataSet, ranges, minVals, m
```
