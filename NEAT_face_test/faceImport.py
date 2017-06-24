#! python3
#Woradorn K.

import numpy as np
#Data from https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data
#mood: (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral)
def faceReader(fName):
    fIn = open(fName, 'r')
    fIn.readline() #strip header line
    faceArr = []
    moodArr = []
    for line in fIn:
        lineArr = line.strip().split(',')
        #face = np.reshape(np.fromstring(lineArr[1], dtype=int, sep=' '), (48,48))
        face = np.fromstring(lineArr[1], dtype=int, sep=' ')
        mood = [-1]*7
        mood[int(lineArr[0])] = 1
        faceArr.append(face)
        moodArr.append(mood)
    pairArr = list(zip(faceArr, moodArr))
    return (faceArr, moodArr)