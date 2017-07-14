#! python3
#Woradorn K.
import numpy as np

toBCD = {
    0:[0,0,0,0],
    1:[0,0,0,1],
    2:[0,0,1,0],
    3:[0,0,1,1],
    4:[0,1,0,0],
    5:[0,1,0,1],
    6:[0,1,1,0],
    7:[0,1,1,1],
    8:[1,0,0,0],
    9:[1,0,0,1],
}
BCDcache = {}
class dataGen:
    trainSet = [[],[]]
    testSet = [[],[]]
    pick = None
    def __init__(self, digits = 2, trainCount = 5, pick = None):
        if pick is None:
            self.pick = []
            while len(self.pick) < trainCount:
                r = np.random.randint(10**(2*digits))
                if not r in self.pick:
                    self.pick.append(r)
        else:
            self.pick = pick
            
        for i in range(10**digits):
            for j in range(10**digits):
                inp = int2bcd(i) + int2bcd(j)
                out = int2bcd(i+j)
                if len(out) > 4*digits:
                    out = out[3:]
                else:
                    out = [0]+out
                self.trainSet[0].append(tuple(inp))
                self.trainSet[1].append(tuple(out))
                if i*(10**digits)+j in self.pick:
                    self.testSet[0].append(tuple(inp))
                    self.testSet[1].append(tuple(out))
        
def int2bcd(num):
    if not num in BCDcache:
        out = []
        ns = str(num)
        for d in ns:
            out+=toBCD[int(d)]
        BCDcache[num] = out
    return BCDcache[num]