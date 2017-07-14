#! python3

import pprint
import array
import numpy as np
#import sklearn.preprocessing as skpr
def dataRead(fName):
    #fIn = open('dataset//smallSet.txt', 'r')
    fIn = open(fName, 'r')
    dataDictRaw = {}
    dataDictNorm = {}
    hdr = fIn.readline().strip().split(',')
    hdr = list(map(str.strip, hdr))
    #toTransform = ['f2','f4','f6','f7','f8','f9','f10','f14']
    #print(hdr)
    for h in hdr:
        dataDictRaw[h] = []
        if not h == 'f12':
            dataDictNorm[h] = []
    for line in fIn: 
        lineArr = line.strip().split(',')
        #print(lineArr)
        for h in hdr:
            #if h in toTransform:
            if False:
                dataDictRaw[h].append(lineArr.pop(0).strip().lstrip())
            else:
                dataDictRaw[h].append(float(lineArr.pop(0).strip().lstrip()))
    #now wrap 'f12' in as -'f11'
    dataDictRaw.pop('mr00')
    dataDictRaw.pop('mr15')
    dataDictRaw.pop('mr60')
    
    dataDictRaw['dewDepr'] = np.subtract(dataDictRaw['temp'],dataDictRaw['dewpoint'])
    dataDictRaw.pop('dewpoint')
    dataDictRaw['baro'] = np.subtract(dataDictRaw['baro'], 29.92)
    data = dataDictRaw
    dataMerged = np.array(list(zip(
                data['hour'],
                data['windN'],
                data['windE'],
                data['gust'],
                data['visibility'],
                data['cloudCover'],
                data['temp'],
                data['dewDepr'],
                data['baro'],
                data['flightRate'],
    )))
    return dataMerged, data['mr30']
