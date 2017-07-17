#! python2
#Woradorn K.
import pprint
import random
import math
import numpy as np
dirMap = {0:(-1,0), 1:(0,1), 2:(1,0), 3:(0,-1)}
decrementSnek = np.vectorize(lambda v: (v-1) if v>0 else v)
rMatCache = {}
class gameState:
    gameGrid = []
    snakeDir = 0 #hdg/90
    score = 0
    runTime = 0
    dead = False
    _localTime = 0
    _timeLimit = 10
    _gridSize = (0,0)
    _foodCount = 0
    _foodLoc = (0,0)
    _headLoc = (0,0)
    _rng = random
    def __init__(self, w = 10, h = 10, seed = 0, start = (5,5), timeLimit = 10):
        self._gridSize = (w,h)
        self._rng.seed(seed)
        self.gameGrid = np.zeros(self._gridSize)
        self.gameGrid[start] = 1
        self._headLoc = (start)
        self._placeFood()
        self._timeLimit = timeLimit
        self._localTime = self._timeLimit
    def run(self, ctrlIn):
        #ctrlIn = {-1: turn left, 0: no turn, 1: turn right}
        assert (-1<=ctrlIn<=1), 'Invalid input'
        assert (not self.dead), 'Dead snake. Please replace gameState object.'
        self.snakeDir += ctrlIn
        self.snakeDir %= 4
        dPos = dirMap[self.snakeDir]
        newPos = tuple(np.mod(np.add(self._headLoc, dPos), self._gridSize))
        lookAhead = self.gameGrid[newPos]
        #print('lookahead at {} saw {}'.format(newPos,lookAhead))
        #assert(lookAhead <= 0), 'Ate self, died.'
        if lookAhead > 1: #If see 1, tail will stay *just* clear of the mouth
            print('dead')
            self.dead = True
            return self.score
        if self._localTime <= 0:
            print('time out')
            self.dead = True
            return self.score
        self.runTime += 1
        #TODO: Death logic
        if lookAhead == -1:
            print('GOT FOOD')
            self.score += 1
            self._foodCount-= 1
            self._placeFood()
            self._localTime = self._timeLimit
        else:
            #now decrement snek
            #print('decrement snake')
            self._localTime -= 1
            self.gameGrid=decrementSnek(self.gameGrid)
        #print('add snake')
        self.gameGrid[newPos] = self.score + 2
        self._headLoc = newPos
        self.printState()
        return -1
        
    def look(self):
        #return what snake see
        fu = self.gameGrid
        #now turn fu into subset
        fu = np.tile(fu, (3,3))
        fuc = np.add(self._headLoc,self._gridSize)
        width = 2
        fu = fu[fuc[0]-width:fuc[0]+width+1,fuc[1]-width:fuc[1]+width+1]
        for i in range(self.snakeDir):
            fu = np.rot90(fu)
        brg = self._getBrg()
        return (fu, brg)
        
    def printState(self):
        print('hdg: {}'.format(self.snakeDir))
        print('score: {}'.format(self.score))
        print('brg: {}'.format(self._getBrg()))
        print('runT: {}'.format(self.runTime))
        print('locT: {}'.format(self._localTime))
        #pprint.pprint(self.gameGrid)
        #do fwd up
        pprint.pprint(self.gameGrid)
        l = self.look()
        pprint.pprint(l[1])
        pprint.pprint(l[0])
        
    def _placeFood(self):
        if self._foodCount >= 1:
            return
        while self._foodCount < 1:
            foodX = self._rng.randint(0,self._gridSize[0]-1)
            foodY = self._rng.randint(0,self._gridSize[1]-1)
            print('put food at {}'.format((foodX, foodY)))
            if self.gameGrid[foodX][foodY] == 0:
                self._foodLoc =(foodX,foodY)
                self._foodCount += 1
                self.gameGrid[foodX][foodY] = -1
                return
    def _getBrg(self):
        #get relative loc of food
        #get world frame vector
        dR = np.subtract(self._foodLoc, self._headLoc)
        dx = min(dR[0], self._gridSize[0] - dR[0], key = abs)
        dy = min(dR[1], self._gridSize[1] - dR[1], key = abs)
        dr = [[dx],[dy]] #in world frame
        #TODO: Cache matrix
        if self.snakeDir not in rMatCache:
            rMatCache[self.snakeDir] = [[-int(math.cos(math.radians(90*self.snakeDir))), int(math.sin(math.radians(90*self.snakeDir)))],
                    [int(math.sin(math.radians(90*self.snakeDir))), int(math.cos(math.radians(90*self.snakeDir)))]]
        dr = np.dot(rMatCache[self.snakeDir], dr).flatten()
        return dr