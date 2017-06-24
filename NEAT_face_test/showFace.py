#! python3
#Woradorn K.
import matplotlib.pyplot as plt
import numpy as np

fIn = open('subset.csv','r')
fIn.readline()
line = fIn.readline().strip().split(',')[1]
lineArr = np.fromstring(line, dtype=int, sep=' ')
lineArr = np.reshape(lineArr, (48,48))
print(lineArr)
plt.imshow(lineArr)
plt.show()