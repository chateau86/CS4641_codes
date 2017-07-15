#! python3
#Woradorn K.
import numpy as np
from pprint import pprint
import dataGen
d = dataGen.dataGen(digits = 2, trainCount = 3)
#pprint(d.trainSet)
print(len(d.trainSet[0]))
#print('---')
pprint(d.testSet)
print(dataGen.int2bcd(21, digits = 2, carryOut = True))
print(dataGen.int2bcd(4, digits = 2, carryOut = True))
print(dataGen.int2bcd(25, digits = 2, carryOut = True))