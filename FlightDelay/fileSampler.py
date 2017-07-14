#! python3
import pprint
import array
import numpy as np
import fileRead

def sample(fName, buckets = 3):
    dataArr = []
    dataIn, rateOut = fileRead.dataRead(fName)
    for i in range(buckets+1):
        dataArr.append([[],[]])
    ind = 0
    try:
        while True:
            for i in range(buckets+1):
                dataArr[i][0].append(dataIn[ind])
                dataArr[i][1].append(rateOut[ind])
                ind += 1
    except Exception as e:
        #print(e)
        pass
    return dataArr