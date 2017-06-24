#! python3
#Woradorn K.

fIn = open('fer2013.csv','r')
fOut = open('subset.csv','w')
start = 0
num = 50
fOut.write(fIn.readline())
for ind in range(start):
    fIn.readline()
for ind in range(num):
    fOut.write(fIn.readline())