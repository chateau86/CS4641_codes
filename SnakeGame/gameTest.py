#! python2
#Woradorn K.
import pprint
import game
g = game.gameState()
g.printState()
g.score = 7
while True:
    for i in range(10):
        g.run(0)
        g.printState()
    g.run(1)
    g.printState()
    g.run(-1)
    g.printState()