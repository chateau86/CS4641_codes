#! python2
#Woradorn K.
import pprint
import game
from pygame.locals import *
import pygame
import time

def visualizeGame(input_array):
	class Pixel:
		x = 1
		y = 1
		color = 1.0

	class App:
			windowWidth = 600
			windowHeight = 600

			def __init__(self):
				self._running = True
				self._display_surf = None
				self._image_surf = None
				self._image_food = None
				self._image_snake = None
				self.matrix = [[0 for x in range(10)] for y in range(10)]

	     
			def load_values(self, input_array):

				pixelWidth, pixelHeight = 600/len(input_array), 600/len(input_array[0])

				rowCount = 0
				for row in input_array:
					rowNum = rowCount * pixelHeight
					rowCount += 1
					
					colCount = 0
					for col in row:
						colNum = colCount * pixelWidth
						colCount += 1
						self.matrix[rowCount - 1][colCount - 1] = (rowNum, colNum, col)


			def on_init(self):
				pygame.init()
				self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
				self._running = True
				self._image_surf = pygame.image.load("blackbox.png").convert()
				self._image_food = pygame.image.load("redbox.png").convert()
				self._image_snake = pygame.image.load("greenbox.png").convert()
	     
			def on_loop(self):
				pass
	     
			def on_render(self):

				self._display_surf.fill((50,50,50))
				# print self.matrix
				for row in self.matrix:
					for pixel in row:
						if pixel[2] < 0:
							self._display_surf.blit(self._image_food,(pixel[0],pixel[1]))
						if pixel[2] == 0:
							self._display_surf.blit(self._image_surf,(pixel[0],pixel[1]))
						if pixel[2] > 0:
							self._display_surf.blit(self._image_snake,(pixel[0],pixel[1]))
				pygame.display.flip()
	     
			def on_cleanup(self):
				pygame.quit()

			def on_execute(self):
				if self.on_init() == False:
					self._running = False

				while( self._running ):
					self.load_values(input_array)
					self.on_loop()
					self.on_render()
					# print "cow"
					# Pause for a second
					time.sleep(1)
					self._running = False
				# self.on_cleanup()
	theApp = App()
	theApp.on_execute()

g = game.gameState()
g.printState()
g.score = 7
while True:
    for i in range(10):
        g.run(0)
        # g.printState()
        # time.sleep(1)
        input_array = g.getState()
        # print "Input Array: ", input_array
        visualizeGame(input_array)

    g.run(1)
    g.printState()
    g.run(-1)
    g.printState()
