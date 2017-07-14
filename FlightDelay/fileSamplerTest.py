#! python3
import pprint
import array
import numpy as np
import fileSampler

dataArr = fileSampler.sample('dataOut.csv')
pprint.pprint(dataArr)