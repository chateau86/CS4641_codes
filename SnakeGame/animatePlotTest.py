#! python2
#Woradorn K.
import game
import animatePlot

g = game.gameState(timeLimit = 9999)
mf = open('test_control.txt', 'r')
m = []
for line in mf:
    m.append(int(line))
#print('m: {}'.format(m))
animatePlot.animate(g,m,'out.mp4')