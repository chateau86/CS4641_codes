#! python2
#Woradorn K.
import pprint
import random

class gameState:
    gameGrid = []
    snakeDir = 0 #hdg/90
    score = 0
    _gridSize = (0,0)
    _foodCount = 0
    _foodLoc = (0,0)
    _rng = random
    def __init__(self, w = 10, h = 10, seed = 0, start = (5,5)):
        self._gridSize = (w,h)
        self._rng.seed(seed)
        for r in range(h):
            self.gameGrid.append([])
            for c in range(w):
                self.gameGrid[r].append(0)
        #pprint.pprint(self.gameGrid)
        self.gameGrid[start[0]][start[1]] = 1
        self._placeFood()
        #print('---')
        #pprint.pprint(self.gameGrid)
    def run(self, ctrlIn):
        #void
        return
        
    def look(self):
        #return what snake see
        return
    def printState(self):
        pprint.pprint(self.gameGrid)
        
    def _placeFood(self):
        if self._foodCount >= 1:
            return
        while self._foodCount < 1:
            foodX = self._rng.randint(0,w)
            foodY = self._rng.randint(0,h)
            if self.gameGrid[foodX][foodY] == 0:
                self._foodLoc =(foodX,foodY)
                self._foodCount += 1
                self.gameGrid[foodX][foodY] = -1
                return
            