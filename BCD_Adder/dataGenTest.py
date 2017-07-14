#! python3
#Woradorn K.
import numpy as np
from pprint import pprint
import dataGen
d = dataGen.dataGen(digits = 3, trainCount = 3)
pprint(d.trainSet)
print(len(d.trainSet[0]))
print('---')
pprint(d.testSet)